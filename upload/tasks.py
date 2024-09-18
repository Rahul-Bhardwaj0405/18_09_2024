# # tasks.py
# from celery import shared_task
# import pandas as pd
# import json
# import logging
# from io import StringIO, BytesIO
# from .models import BookingData, RefundData  # Import new models
# # Updated tasks.py

# @shared_task
# def process_uploaded_files(file_content, file_name, bank_name, year, month, booking_or_refund):
#     try:
#         # Initialize an empty DataFrame
#         df = pd.DataFrame()

#         # Read the file content into a DataFrame based on file type
#         if file_name.endswith('.csv'):
#             df = pd.read_csv(StringIO(file_content.decode('utf-8')))
#             print(df)
#         elif file_name.endswith('.xlsx'):
#             df = pd.read_excel(BytesIO(file_content))
#             print(df)
#         elif file_name.endswith('.txt'):
#             df = pd.read_csv(StringIO(file_content.decode('utf-8')), delimiter='\t')
#         elif file_name.endswith('.json'):
#             data = json.loads(file_content)
#             df = pd.json_normalize(data)
#         else:
#             try:
#                 file_str = file_content.decode('utf-8')
#                 delimiter = ',' if ',' in file_str else '\t'
#                 df = pd.read_csv(StringIO(file_str), delimiter=delimiter)
#             except Exception as e:
#                 logging.error(f"Error converting file {file_name} to CSV: {e}")
#                 return

#         # Extract required columns based on bank and booking/refund
#         try:
#             if bank_name == 'karur_vysya':
#                 # Extract sale total (count of rows)
#                 sale_total = df[df.columns[0]].count()  # Assumes the first column is 'S.NO.'
#                 print(sale_amount)

#                 # Extract date from 'CREDITED ON'
#                 date_column = df['CREDITED ON']
#                 date = pd.to_datetime(date_column.iloc[0]).date()
#                 print(date)

#                 # Extract total sale amount (sum of 'BOOKING AMOUNT')
#                 sale_amount_column = df['BOOKING AMOUNT']
#                 sale_amount = float(sale_amount_column.sum())  # Sum of all booking amounts
#                 print(sale_amount)

#                 # Save to the database
#                 if booking_or_refund == 'booking':
#                     BookingData.objects.create(
#                         bank_name=bank_name,
#                         year=year,
#                         month=month,
#                         sale_total=sale_total,
#                         date=date,
#                         sale_amount=sale_amount
#                     )
#                 # elif booking_or_refund == 'refund':
#                 #     RefundData.objects.create(
#                 #         bank_name=bank_name,
#                 #         year=year,
#                 #         month=month,
#                 #         sale_total=sale_total,
#                 #         date=date,
#                 #         sale_amount=sale_amount
#                 #     )
#                 else:
#                     logging.error(f"Unknown booking_or_refund type: {booking_or_refund}")

#             else:
#                 logging.error(f"Unknown bank type: {bank_name}")

#         except Exception as e:
#             logging.error(f"Error extracting data from file {file_name}: {e}")

#     except Exception as e:
#         logging.error(f"Error processing file {file_name}: {e}")
# tasks.py
from celery import shared_task
import pandas as pd
import json
import logging
from io import StringIO, BytesIO
from .models import BookingData  # Import new models

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@shared_task
def process_uploaded_files(file_content, file_name, bank_name, year, month, booking_or_refund):
    logging.info(f"Processing file: {file_name} with bank_name: {bank_name}, year: {year}, month: {month}, booking_or_refund: {booking_or_refund}")

    try:
        # Initialize an empty DataFrame
        df = pd.DataFrame()

        # Read the file content into a DataFrame based on file type
        if file_name.endswith('.csv'):
            df = pd.read_csv(StringIO(file_content.decode('utf-8')))
            logging.info("CSV file read successfully.")
        elif file_name.endswith('.xlsx'):
            df = pd.read_excel(BytesIO(file_content))
            logging.info("Excel file read successfully.")
        elif file_name.endswith('.txt'):
            df = pd.read_csv(StringIO(file_content.decode('utf-8')), delimiter='\t')
            logging.info("TXT file read successfully.")
        elif file_name.endswith('.json'):
            data = json.loads(file_content)
            df = pd.json_normalize(data)
            logging.info("JSON file read successfully.")
        else:
            try:
                file_str = file_content.decode('utf-8')
                delimiter = ',' if ',' in file_str else '\t'
                df = pd.read_csv(StringIO(file_str), delimiter=delimiter)
                logging.info("Non-standard file read successfully.")
            except Exception as e:
                logging.error(f"Error converting file {file_name} to CSV: {e}")
                return

        # Clean the column names to remove unwanted spaces and periods
        df.columns = df.columns.str.strip().str.replace('.', '', regex=False)
        logging.info(f"Column names cleaned: {df.columns.tolist()}")

        # Extract required columns based on bank and booking/refund
        try:
            if bank_name == 'karur_vysya':
                # Extract sale total (count of rows)
                sale_total = df['SNO'].count()  # Assumes the first column is 'S.NO.'
                logging.info(f"Sale Total: {sale_total}")

                # Extract date from 'CREDITED ON'
                date_column = df['CREDITED ON']
                date = pd.to_datetime(date_column.iloc[0]).date()
                logging.info(f"Date: {date}")

                # Extract total sale amount (sum of 'BOOKING AMOUNT')
                sale_amount_column = df['BOOKING AMOUNT']
                sale_amount = float(sale_amount_column.sum())  # Sum of all booking amounts
                logging.info(f"Sale Amount: {sale_amount}")

                # Save to the database
                if booking_or_refund == 'booking':
                    BookingData.objects.create(
                        bank_name=bank_name,
                        year=year,
                        month=month,
                        sale_total=sale_total,
                        date=date,
                        sale_amount=sale_amount
                    )
                    logging.info(f"Booking data saved successfully for file: {file_name}.")
                else:
                    logging.error(f"Unknown booking_or_refund type: {booking_or_refund}")

            else:
                logging.error(f"Unknown bank type: {bank_name}")

        except Exception as e:
            logging.error(f"Error extracting data from file {file_name}: {e}")

    except Exception as e:
        logging.error(f"Error processing file {file_name}: {e}")
