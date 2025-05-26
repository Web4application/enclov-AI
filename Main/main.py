from fastapi import FastAPI
from kubernetes import client, config

app = FastAPI()

@app.get("/k8s/nodes")
def list_nodes():
    try:
        config.load_kube_config()  # Use load_incluster_config() if running inside k8s pod
        v1 = client.CoreV1Api()
        nodes = v1.list_node()
        node_names = [node.metadata.name for node in nodes.items]
        return {"nodes": node_names}
    except Exception as e:
        return {"error": str(e)}
