"""
PDF Studio - Módulo de Conversão PDF para Excel
Funcionalidades para extração de tabelas e conversão para Excel
"""

import os
import pdfplumber
import tabula
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
import re
from .pdf_utils import generate_unique_filename, cleanup_file

class PDFConverter:
    def __init__(self, upload_folder, output_folder):
        self.upload_folder = upload_folder
        self.output_folder = output_folder
    
    def parse_text_to_table(self, text):
        """Parse text content to extract structured data as table"""
        lines = text.strip().split('\n')
        table_data = []
        
        # Try to detect patterns like the example shown
        # Pattern: ID + Description + Unit + Value + Date
        # Followed by: Company + Unit + Value + Value + Percentages
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
                
            # Check if this line starts with a pattern like "10 13866" (ID + number)
            if re.match(r'^\d+\s+\d+', line):
                # This looks like a main item line
                parts = line.split()
                
                if len(parts) >= 5:
                    # Extract ID, description, unit, value, date
                    item_id = f"{parts[0]} {parts[1]}"
                    
                    # Find description (everything between ID and the last 3 parts)
                    desc_parts = parts[2:-3]
                    description = ' '.join(desc_parts)
                    
                    # Last 3 parts should be unit, value, date
                    unit = parts[-3]
                    value = parts[-2]
                    date = parts[-1]
                    
                    # Look for the next line (company info)
                    company_info = ""
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        if next_line and not re.match(r'^\d+\s+\d+', next_line):
                            company_info = next_line
                            i += 1  # Skip the next line as we processed it
                    
                    # Create table row
                    if company_info:
                        # Split company info into parts
                        company_parts = company_info.split()
                        if len(company_parts) >= 5:
                            company_name = ' '.join(company_parts[:-4])  # Everything except last 4 parts
                            company_unit = company_parts[-4]
                            company_value1 = company_parts[-3]
                            company_value2 = company_parts[-2]
                            percentages = company_parts[-1]
                            
                            table_data.append([
                                item_id,
                                description,
                                unit,
                                value,
                                date,
                                company_name,
                                company_unit,
                                company_value1,
                                company_value2,
                                percentages
                            ])
                        else:
                            # Fallback: just add company info as one field
                            table_data.append([
                                item_id,
                                description,
                                unit,
                                value,
                                date,
                                company_info,
                                "", "", "", ""
                            ])
                    else:
                        # No company info, just main item
                        table_data.append([
                            item_id,
                            description,
                            unit,
                            value,
                            date,
                            "", "", "", "", ""
                        ])
            
            i += 1
        
        # If we found data, add headers
        if table_data:
            headers = [
                "ID",
                "Descrição",
                "Unidade",
                "Valor",
                "Data",
                "Empresa",
                "Unidade Empresa",
                "Valor 1",
                "Valor 2",
                "Percentagens"
            ]
            return [headers] + table_data
        
        # If no structured data found, try a more generic approach
        return self.parse_generic_text_to_table(text)
    
    def parse_generic_text_to_table(self, text):
        """Generic text parsing for any structured data"""
        lines = text.strip().split('\n')
        table_data = []
        
        # Look for any lines that contain multiple data points separated by spaces
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Split by multiple spaces to find data columns
            parts = re.split(r'\s{2,}', line)  # Split by 2 or more spaces
            
            if len(parts) >= 3:  # At least 3 columns of data
                # Clean up each part
                cleaned_parts = [part.strip() for part in parts if part.strip()]
                if len(cleaned_parts) >= 3:
                    table_data.append(cleaned_parts)
        
        # If we found data, create headers
        if table_data:
            max_cols = max(len(row) for row in table_data)
            headers = [f"Coluna {i+1}" for i in range(max_cols)]
            
            # Pad rows to have same number of columns
            padded_data = []
            for row in table_data:
                padded_row = row + [""] * (max_cols - len(row))
                padded_data.append(padded_row)
            
            return [headers] + padded_data
        
        return None
    
    def extract_tables_pdfplumber(self, pdf_path):
        """Extract tables using pdfplumber - primary method"""
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # First try to extract structured tables
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table_num, table in enumerate(page_tables):
                            if table and len(table) > 1:  # Ensure table has data
                                # Clean the table data
                                cleaned_table = []
                                for row in table:
                                    if row:  # Skip empty rows
                                        cleaned_row = [cell.strip() if cell else '' for cell in row]
                                        cleaned_table.append(cleaned_row)
                                
                                if cleaned_table:
                                    tables.append({
                                        'page': page_num + 1,
                                        'table': table_num + 1,
                                        'data': cleaned_table
                                    })
                    
                    # If no structured tables found, try to extract text and parse it
                    if not page_tables:
                        text = page.extract_text()
                        if text:
                            parsed_data = self.parse_text_to_table(text)
                            if parsed_data:
                                tables.append({
                                    'page': page_num + 1,
                                    'table': 1,
                                    'data': parsed_data
                                })
        except Exception as e:
            print(f"Error with pdfplumber: {e}")
            return None
        return tables
    
    def extract_tables_tabula(self, pdf_path):
        """Extract tables using tabula-py - fallback method"""
        tables = []
        try:
            # Try to extract all tables from all pages
            dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
            
            for page_num, df in enumerate(dfs):
                if not df.empty:
                    # Convert DataFrame to list of lists
                    table_data = [df.columns.tolist()] + df.values.tolist()
                    
                    # Clean the data
                    cleaned_table = []
                    for row in table_data:
                        cleaned_row = [str(cell).strip() if pd.notna(cell) else '' for cell in row]
                        cleaned_table.append(cleaned_row)
                    
                    tables.append({
                        'page': page_num + 1,
                        'table': 1,
                        'data': cleaned_table
                    })
        except Exception as e:
            print(f"Error with tabula: {e}")
            # If tabula fails due to Java issues, try text extraction as fallback
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            parsed_data = self.parse_text_to_table(text)
                            if parsed_data:
                                tables.append({
                                    'page': page_num + 1,
                                    'table': 1,
                                    'data': parsed_data
                                })
            except Exception as e2:
                print(f"Error with text extraction fallback: {e2}")
                return None
        return tables
    
    def create_excel_file(self, tables, output_path):
        """Create Excel file with proper formatting"""
        wb = Workbook()
        
        # Remove default sheet
        wb.remove(wb.active)
        
        for table_info in tables:
            table_data = table_info['data']
            page_num = table_info['page']
            table_num = table_info['table']
            
            # Create sheet name
            if len(tables) == 1:
                sheet_name = f"Page_{page_num}"
            else:
                sheet_name = f"Page_{page_num}_Table_{table_num}"
            
            # Ensure sheet name is valid (max 31 chars)
            sheet_name = sheet_name[:31]
            
            ws = wb.create_sheet(title=sheet_name)
            
            # Add data to worksheet
            for row_idx, row in enumerate(table_data, 1):
                for col_idx, cell_value in enumerate(row, 1):
                    ws.cell(row=row_idx, column=col_idx, value=cell_value)
            
            # Format header row
            if table_data:
                header_row = 1
                for col_idx in range(1, len(table_data[0]) + 1):
                    cell = ws.cell(row=header_row, column=col_idx)
                    cell.font = Font(bold=True)
                    cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
                    cell.alignment = Alignment(horizontal="center")
            
            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                ws.column_dimensions[column_letter].width = adjusted_width
        
        wb.save(output_path)
    
    def convert_pdf_to_excel(self, pdf_path):
        """
        Converte PDF para Excel
        
        Args:
            pdf_path: Caminho do PDF
            
        Returns:
            tuple: (success, excel_path, error_message)
        """
        try:
            # Gerar nome único para arquivo Excel
            excel_filename, file_id = generate_unique_filename("converted.xlsx")
            excel_path = os.path.join(self.output_folder, excel_filename)
            
            # Extract tables using pdfplumber first
            tables = self.extract_tables_pdfplumber(pdf_path)
            
            # If pdfplumber fails, try tabula
            if not tables:
                tables = self.extract_tables_tabula(pdf_path)
            
            if not tables:
                return False, None, "Nenhuma tabela encontrada no PDF. Certifique-se de que o PDF contém dados tabulares."
            
            # Create Excel file
            self.create_excel_file(tables, excel_path)
            
            return True, excel_path, None
            
        except Exception as e:
            return False, None, f"Erro ao converter PDF: {str(e)}"

