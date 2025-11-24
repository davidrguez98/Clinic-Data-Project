class DataTransformer:

    # Agrupa a los trabajadores y sus citas
    @staticmethod
    def workers_processed(raw_workers_data):
        grouped = {}

        for name, time, reason in raw_workers_data:
            if name not in grouped:
                grouped[name] = []
            grouped[name].append({
                "time": time,
                "reason": reason
            })

        return grouped
    
    # Formatea los datos en la estructura para guardarlos
    @staticmethod
    def format_daily_data(date, appointments_count, workers_data, billing_total):

        return {
            "date": date,
            "appointments_count": appointments_count,
            "workers_data": workers_data,
            "billing_total": billing_total
        }