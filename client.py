import grpc
import egapro_pb2
import egapro_pb2_grpc

def run():
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            print("Connexion au serveur...")
            stub = egapro_pb2_grpc.EgaProServiceStub(channel)
            
            siren = input("Entrez le SIREN : ")
            response = stub.GetEgaProData(egapro_pb2.EgaProRequest(siren=siren))
            
            print(f"Entreprise : {response.entreprise}")
            print(f"Région : {response.region}")
            print(f"Département : {response.departement}")
            print(f"Index : {response.index}")

    except grpc.RpcError as e:
        print(f"Erreur gRPC : {e.code()} - {e.details()}")

if __name__ == "__main__":
    run()
