import boto3
import time

# Configuración de Boto3
ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')
cloudwatch_client = boto3.client('cloudwatch')

# Función para generar reporte de uso de recursos de EC2 (CPU, Memoria)
def generate_ec2_report(instance_ids):
    report = {}
    
    for instance_id in instance_ids:
        print(f"Recopilando métricas para la instancia {instance_id}...")
        
        # Obtener métricas de CPU
        cpu_metrics = cloudwatch_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'cpu_usage',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/EC2',
                            'MetricName': 'CPUUtilization',
                            'Dimensions': [
                                {
                                    'Name': 'InstanceId',
                                    'Value': instance_id
                                }
                            ]
                        },
                        'Period': 300,
                        'Stat': 'Average',
                    },
                    'ReturnData': True
                },
            ],
            StartTime=time.time() - 3600,  # Última hora
            EndTime=time.time(),
        )
        
        cpu_usage = cpu_metrics['MetricDataResults'][0]['Values']
        report[instance_id] = {
            'CPU_Usage': cpu_usage if cpu_usage else 'No Data'
        }
    
    return report

# Listar los buckets de S3 y sus objetos
def list_s3_buckets_and_objects():
    print("Listando los buckets de S3...")
    buckets = s3_client.list_buckets()
    
    s3_report = {}
    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        print(f"Bucket encontrado: {bucket_name}")
        
        # Listar objetos dentro del bucket
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        objects_list = []
        if 'Contents' in objects:
            for obj in objects['Contents']:
                objects_list.append(obj['Key'])
        
        s3_report[bucket_name] = objects_list
    
    return s3_report

# Función principal para automatizar las tareas
def main():
    # Lista de instancias EC2 existentes
    instance_ids = [
        'i-0d0e6f5b3ef84e172',
        'i-05ef637a44ee8cf8a', 
        'i-05682b4617b38c0e1',
        'i-0585bbd13afde5834',
        'i-0b517f9d1fd37723c',
        'i-0a238ca17083e92b5',
        'i-026f6d42238201340',
        'i-0c3db67ca87e55382',
        'i-0120d048ff69d3dd6'
    ]
    
    print(f"Instancias EC2 a monitorear: {instance_ids}")
    
    # Generar reporte de uso de recursos de EC2
    ec2_report = generate_ec2_report(instance_ids)
    print("Reporte de uso de recursos de EC2:", ec2_report)
    
    # Listar buckets de S3 y sus objetos
    s3_report = list_s3_buckets_and_objects()
    print("Reporte de buckets S3:", s3_report)

if __name__ == "__main__":
    main()
