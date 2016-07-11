
https://docs.docker.com/engine/installation/linux/debian/
gcloud init
gcloud container clusters get-credentials CLUSTERNAME

wget https://github.com/kubernetes/kubernetes/releases/download/v1.3.0/kubernetes.tar.gz

## Proxy

gcloud docker push gcr.io/$PROJECT_ID/allservices:v1
docker build -t gcr.io/$PROJECT_ID/allservices:v1 .

docker build -t gcr.io/$PROJECT_ID/proxy:v1 .
gcloud docker push gcr.io/$PROJECT_ID/proxy:v1

docker build -t gcr.io/$PROJECT_ID/scipy-app:v1 .
gcloud docker push gcr.io/$PROJECT_ID/scipy-app:v1
```
kubectl create -f proxy-app.yml
```

## UI

Edit `ui-app.yml` to have the Kubernetes auth info

```
kubectl create -f ui-app.yml
```
