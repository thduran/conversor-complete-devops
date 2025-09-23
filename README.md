Texto em pt-br logo abaixo!

# Converter API - DevOps End-to-End (Portfolio)

## 1. About the project

This project was developed as a **complete step-by-step DevOps implementation**, covering:

- Containerization (Docker)
- Automated testing
- CI/CD with GitHub Actions
- Deployment on Kubernetes (staging and production)
- Monitoring with Prometheus and Grafana
- Alerts via Alertmanager integrated with Slack
- Managed PostgreSQL database (DigitalOcean)


⚠️ **Important**: the main goal is not the **usability of the application** itself, but to demonstrate a full DevOps pipeline from scratch to production.

## 2. What the project does

- Provides a simple conversion API (`/converter`)
- Stores conversion history (`/history`) in PostgreSQL
- Exposes metrics via Prometheus (`/metrics`)
- Automates build, test and deploy with GitHub Actions
- Enables observability with Grafana and alerts on Slack

---

## 3. Note on usability

This project was **not made for commercial or real production use**.
Features like conversion or history are **educational examples**.
The real value of the project is to demonstrate:

- Automated CI/CD
- Secure deployment on Kubernetes
- Observability
- Integrated alerts
- Managed database in the cloud

## 4. How to test the project

### 4.1 Prerequisites

- Kubernetes cluster (DigitalOcean, Minikube or Kind)
- Configured `kubectl`
- Docker Hub account
- Slack account for alerts (or another service)
👉 **Optional**: Python 3.11 if you want to run the API locally

## 4.2 Clone the repository
```bash
git clone https://github.com/thduran/conversor-complete-devops.git
cd conversor-complete-devops
```

---

### 4.3 Configure secrets

#### Database
Create a secret for the PostgreSQL database:
```bash
export DB_URL="postgresql://user:password@host:port/database"
kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL="$DB_URL" \
  -n staging

kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL="$DB_URL" \
  -n production
```

- DO_ACCESS_TOKEN → DigitalOcean
- DOCKER_USERNAME and DOCKER_PASSWORD → Docker Hub
- CLUSTER_KUBECONFIG → your cluster kubeconfig in base64

#### Grafana (optional)
```bash
export GRAFANA_PASSWORD="your_password"
kubectl create secret generic grafana-admin \
  --from-literal=password="$GRAFANA_PASSWORD" \
  -n monitoring
```
### 4.4 Run the app locally (optional)
```bash
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```

- API available at http://localhost:8000
- Test /converter and /history

### 4.5 Manual deploy (without CI/CD)

1. Create namespaces and apply Secrets
```bash
kubectl apply -f k8s/base
```

2. Deploy database, API, Prometheus and Grafana:
```bash
kubectl apply -f k8s/base/staging
kubectl apply -f k8s/base/production
kubectl apply -f k8s/base/monitoring
```

3. Check pods and services:
```bash
kubectl get pods -n staging
kubectl get pods -n production
kubectl get svc -n staging
kubectl get svc -n production
```

4. Test with LoadBalancer IPs
http://<IP_STAGING>/converter?value=10&from=usd&to=brl
http://<IP_PRODUCTION>/converter?value=20&from=eur&to=brl
http://<IP_PRODUCTION>/history

### 4.6 CI/CD

The GitHub Actions workflow (.github/workflows/ci-cd.yaml) performs:
- Docker image build and push to Docker Hub
- Automatic deploy to staging (production requires manual approval)

### 4.7 Observability

- Prometheus → http://<IP_PROMETHEUS>:9090
- Grafana → http://<IP_GRAFANA>:3000
- Alertmanager → sends alerts to the configured Slack channel

✅ Conclusion

This project demonstrates the complete DevOps cycle in practice:

- Docker: application containerization
- GitHub Actions: CI/CD pipeline
- Kubernetes: staging + production with load balancing
- Prometheus & Grafana: metrics and dashboards
- Alertmanager: alerts integrated with Slack
- PostgreSQL: managed cloud database

It is a learning and portfolio project, showcasing real hands-on experience with modern DevOps from scratch to production.

PT-BR:

# Conversor API - DevOps End-to-End (Portfólio)

## 1. Sobre o projeto

Este projeto foi desenvolvido como um **passo a passo completo de DevOps**, cobrindo:

- Containerização (Docker)
- Testes automatizados
- CI/CD com GitHub Actions
- Deploy em Kubernetes (staging e produção)
- Monitoramento com Prometheus e Grafana
- Alertas via Alertmanager integrado ao Slack
- Banco de dados PostgreSQL gerenciado (DigitalOcean Managed DB)

⚠️ **Importante:** o objetivo **não é a usabilidade da aplicação em si**, mas sim demonstrar um **pipeline DevOps completo do zero até produção**.

---

## 2. O que o projeto faz

- Exibe uma API de conversão simples (`/converter`)
- Salva histórico de conversões (`/history`) em PostgreSQL
- Expõe métricas via Prometheus (`/metrics`)  
- Automatiza build, teste e deploy com GitHub Actions  
- Permite observabilidade via Grafana e alertas no Slack

---

## 3. Atenção sobre usabilidade

Este projeto **não foi feito para uso comercial ou produção real**.  
Funcionalidades como conversão ou histórico são **exemplos didáticos**.  
O valor do projeto está em mostrar:

- CI/CD automatizado   
- Deploy seguro em Kubernetes  
- Observabilidade
- Alertas integrados
- BD gerenciado em cloud

---

## 4. Como testar o projeto

### 4.1 Pré-requisitos

- Cluster Kubernetes (DigitalOcean, Minikube ou Kind)
- `kubectl` configurado  
- Conta no Docker Hub 
- Conta no Slack pra alertas (ou outro)
👉 **Opcional**: Python 3.11 se quiser rodar a API localmente.

### 4.2 Clone o repositório
```bash
git clone https://github.com/thduran/conversor-complete-devops.git
cd conversor-complete-devops
```

---

### 4.3 Configurar secrets

#### Banco de dados
Crie um secret pro banco PostgreSQL:

```bash
export DB_URL="postgresql://usuario:senha@host:porta/banco"
kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL="$DB_URL" \
  -n staging

kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL="$DB_URL" \
  -n production
```

- DO_ACCESS_TOKEN → DigitalOcean
- DOCKER_USERNAME e DOCKER_PASSWORD → Docker Hub
- CLUSTER_KUBECONFIG → kubeconfig do cluster em base64

#### Grafana (opcional)
```bash
export GRAFANA_PASSWORD="sua_senha"
kubectl create secret generic grafana-admin \
  --from-literal=password="$GRAFANA_PASSWORD" \
  -n monitoring
```

### 4.4 Rodar a aplicação localmente (opcional)
```bash
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```

- API disponível em http://localhost:8000
- Teste /converter e /history

### 4.5 Deploy manual (sem CI/CD)

1. Criar namespaces e aplicar Secrets
```bash
kubectl apply -f k8s/base
```

2. Deploy do banco, API, Prometheus e Grafana:
```bash
kubectl apply -f k8s/base/staging
kubectl apply -f k8s/base/production
kubectl apply -f k8s/base/monitoring
```

3. Verificar pods e serviços:
```bash
kubectl get pods -n staging
kubectl get pods -n production
kubectl get svc -n staging
kubectl get svc -n production
```

4. Teste com IPs do LoadBalancer

http://<IP_STAGING>/converter?value=10&from=usd&to=brl
http://<IP_PRODUCTION>/converter?value=20&from=eur&to=brl
http://<IP_PRODUCTION>/history

### 4.6 CI/CD

O workflow GitHub Actions (.github/workflows/ci-cd.yaml) faz:
- Build e push de imagem Docker para Docker Hub
- Deploy automático para staging (produção requer aprovação manual)

### 4.7 Observabilidade

- Prometheus → http://<IP_PROMETHEUS>:9090
- Grafana → http://<IP_GRAFANA>:3000
- Alertmanager → envia alertas para o canal Slack configurado

✅ Conclusão

Este projeto mostra na prática o ciclo DevOps completo:

- Docker: containerização da aplicação
- GitHub Actions: pipeline CI/CD
- Kubernetes: staging + produção com balanceador de carga
- Prometheus & Grafana: métricas e dashboards
- Alertmanager: alertas integrados ao Slack
- PostgreSQL: banco de dados gerenciado em cloud

É um projeto de aprendizado e portfólio, mostrando experiência real em DevOps moderno do zero até produção.