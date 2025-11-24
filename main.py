from ETL.extract import DataExtractor
from ETL.transform import DataTransformer
from ETL.load import DataLoader

# Ejecuta el proceso ETL completo
def run_etl_process():

    print("INICIANDO EL PROCESO ETL")

    # EXTRACT - Extracción de datos (Uso una fecha forzada para crear el ejemplo)
    extractor = DataExtractor(database_name="dental_clinic", test_date="2025-11-15")

    appointments_count = extractor.get_appointments_count()
    workers_raw = extractor.get_workers_raw_data()
    billing_total = extractor.get_billing_total()

    # TRANSFORM - Procesamiento de datos
    transformer = DataTransformer()

    workers_data = transformer.workers_processed(workers_raw)
    final_data = transformer.format_daily_data(
        date=extractor.today,
        appointments_count=appointments_count,
        workers_data=workers_data,
        billing_total=billing_total
    )

    # LOAD - Carga de datos a Firestore
    loader = DataLoader()
    success = loader.load_daily_information(final_data)

    if success:
        print("Process completed")
    else:
        print("Error during the process")

if __name__ == "__main__":
    run_etl_process()