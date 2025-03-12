import grpc
from concurrent import futures
import pandas as pd
import time

import egapro_pb2
import egapro_pb2_grpc

# Charger les données depuis le CSV
DATA = pd.read_csv("index-egalite-fh 3(Données publiques Index Egapro).csv", encoding='ISO-8859-1')

class EgaProServiceServicer(egapro_pb2_grpc.EgaProServiceServicer):
    def GetEgaProData(self, request, context):
        siren = request.siren
        result = DATA[DATA['SIREN'].astype(str) == siren]

        if not result.empty:
            entreprise = result.iloc[0]['Raison Sociale']
            region = result.iloc[0]['Région']
            departement = result.iloc[0]['Département']
            try:
                index = float(result.iloc[0]['Note Index'])
            except ValueError:
                index = -1.0  # Valeur par défaut si l'index est invalide

            return egapro_pb2.EgaProResponse(
                entreprise=entreprise,
                region=region,
                departement=departement,
                index=index
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("SIREN non trouvé")
            return egapro_pb2.EgaProResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    egapro_pb2_grpc.add_EgaProServiceServicer_to_server(EgaProServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Serveur gRPC démarré sur le port 50051...")
    try:
        while True:
            time.sleep(86400)  # Maintient le serveur actif
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
