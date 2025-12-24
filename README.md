[Para PT-BR, clique aqui](#conversor-api---devops-end-to-end-portfólio)

# Converter API - DevOps End-to-End (Portfolio)

## 1. About the project

This project is a hands-on DevOps lab, simulating a real software lifecycle, covering:

- Containerization (Docker)
- Deploy to Kubernetes (staging and production)
- Scalability (HPA) based on CPU and memory
- CI/CD with GitHub Actions
- Observability with Prometheus and Grafana
- Alertmanager integrated with Slack
- Automated tests

⚠️ The main goal isn't the app itself, but to demonstrate Devops practices fully applied from scratch to production.

## 2. What the project does

- Simple currency conversion API (`/converter`)
- Saves conversion history (`/history`) in PostgreSQL
- Exposes metrics through Prometheus (`/metrics`)
- Automates build, test and deploy with GitHub Actions
- Enables observability through Grafana and alerts in Slack

## 3. How to run the project

### 3.1 Pre-requisites

- Kubernetes cluster (DigitalOcean, minikube, kind)
- `kubectl` configured
- Docker installed
- Slack account (optional, for alerts)

### 3.2 Clone the repo

```bash
git clone https://github.com/thduran/conversor-complete-devops.git
cd conversor-complete-devops
```

### 3.3 Configure secrets

1. Create namespaces
```bash
kubectl apply -f k8s/base
```
#### Database

Create secrets for Postgres

```bash
# admin password (staging and production)
kubectl create secret generic db-admin-pass -n staging --from-literal=PASSWORD="postgres"
kubectl create secret generic db-admin-pass -n production --from-literal=PASSWORD="postgres"

# Application connection string (staging and production)
kubectl create secret generic db-credentials -n staging \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-svc:5432/app_db"
kubectl create secret generic db-credentials -n production \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-svc:5432/app_db"
```

#### Grafana (optional)
```bash
export GRAFANA_PASSWORD="my-password"
kubectl create secret generic grafana-admin \
  --from-literal=password="$GRAFANA_PASSWORD" \
  -n monitoring
```

### 3.4 Manual deploy (without CI/CD)

1. Deploy database, API, Prometheus and Grafana:
```bash
kubectl apply -f k8s/base/staging
kubectl apply -f k8s/base/production
kubectl apply -f k8s/prometheus -R
kubectl apply -f k8s/grafana
```

2. Check pods and services:
```bash
kubectl get pods -n staging
kubectl get pods -n production
kubectl get svc -n staging
kubectl get svc -n production
```

3. Test with LoadBalancer IPs

`http://<IP_STAGING>/converter?value=10&from=usd&to=brl` \
`http://<IP_PRODUCTION>/converter?value=20&from=usd&to=brl` \
`http://<IP_PRODUCTION>/history` 

If you're running it locally: \
`kubectl port-forward -n production svc/conversor 8080:80` \
`kubectl port-forward -n monitoring svc/prometheus 9090:9090` \
`kubectl port-forward -n monitoring svc/grafana 3000:3000`

## 4. Validating elasticity (HPA test)

### 4.1 Open HPA monitoring
`kubectl get hpa -n production -w`

### 4.2 Generate load on the existing pods
`kubectl exec -it conversor-PODNAME -n production -- python -c "while True: 10**1000"`

In Grafana, you'll see the _CPU PER PODS_ chart increasing. As the HPA detects usage spike, you can watch the numbers of replicas increasing in the terminal and in the _NUMBER OF PODS_ chart. _MEMORY_ will remain stable as only CPU is stressed.

## 5. Challenges and learning

- HPA parameters: Grafana was also used to analyze real usage and adjust HPA parameters to fit the app's reality.
- Service Discovery: Prometheus couldn't see new pods. Implemented k8s Service Discovery, so new replicas are automatically detected.
- Secret management: Github blocked pushing secrets. Recreating files with placeholders and using secrets proved to be a best practice.
- Docker Hub scopes: Push was denied (insufficient scopes). Fixed by creating a token with write scope.
- Path context: Github couldn't find the path because push command wasn't executed from the root.
- CI/CD best practices: attempting deployment without tests or approval. Adjusted pipeline to validate CI before proceeding to CD.
- Kubeconfig context: Workflow failed in production jobs (kubectl was connecting to localhost). Set KUBECONFIG variable in all necessary jobs.
- Portability: replaced all hardcoded passwords, IPs, tokens with placeholders or secrets, and clearly documented usage in the README.
- Dependencies: Gunicorn wasn't found because it was missing from requirements.txt

## 6. Visual demo

📄 [CLICK HERE to view pdf evidence: p.1 - database history; p.2- Slack alert; p.3 - Prometheus alert; p.4 - Jobs of Actions; p.5 - Grafana dashboards](docs/img.pdf)

On page 5, observe HPA in action, increasing or decreasing the number of pods as necessary.

### 7. CI/CD

The workflow (.github/workflows/ci-cd.yaml) runs on every push to the main branch and executes:
- Build and push of Docker image to Docker Hub.
- Automatic deploy to Kubernetes staging environment.
- Deploy to production (Digital Ocean) requiring manual approval.
- Automated tests in Python.

### ✅ 8. Conclusion

This project consolidated fundamental knowledge for a DevOps Engineer role, demonstrating the ability to orchestrate, automate and monitor modern applications in containerized environments.

---

PT-BR:

# Conversor - DevOps End-to-End (Portfólio)

## 1. Sobre o projeto

Este projeto é um laboratório prático de DevOps, simulando um ciclo de vida real de software, cobrindo:

- Containerização (Docker)
- Deploy em Kubernetes (staging e produção)
- Escalabilidade (HPA) baseada em CPU e memória
- CI/CD com GitHub Actions
- Monitoramento com Prometheus e Grafana
- Alertmanager integrado ao Slack
- Testes automatizados

⚠️ O objetivo não é a aplicação em si, mas demonstrar a aplicação de práticas DevOps completo do zero até produção.

## 2. O que o projeto faz

- API simples de conversão de moeda (`/converter`)
- Salva histórico de conversões (`/history`) em PostgreSQL
- Expõe métricas via Prometheus (`/metrics`)  
- Automatiza build, teste e deploy com GitHub Actions
- Permite observabilidade via Grafana e alertas no Slack

## 3. Como rodar o projeto

### 3.1 Pré-requisitos

- Cluster Kubernetes (DigitalOcean, minikube, kind)
- `kubectl` configurado  
- Docker instalado 
- Conta no Slack (ou outro) pra alertas

### 3.2 Clone o repositório
```bash
git clone https://github.com/thduran/conversor-complete-devops.git
cd conversor-complete-devops
```

### 3.3 Configurar secrets

1. Criar namespaces
```bash
kubectl apply -f k8s/base
```

#### Banco de dados

Crie as secrets para o Postgres

```bash
# Senha do admin (staging e production)
kubectl create secret generic db-admin-pass -n staging --from-literal=PASSWORD="postgres"
kubectl create secret generic db-admin-pass -n production --from-literal=PASSWORD="postgres"

# Conexão da aplicação (staging e production)
kubectl create secret generic db-credentials -n staging \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-svc:5432/app_db"
kubectl create secret generic db-credentials -n production \
  --from-literal=DATABASE_URL="postgresql://postgres:postgres@postgres-svc:5432/app_db"
```

#### Grafana (opcional)
```bash
export GRAFANA_PASSWORD="my-password"
kubectl create secret generic grafana-admin \
  --from-literal=password="$GRAFANA_PASSWORD" \
  -n monitoring
```

### 3.4 Deploy manual (sem CI/CD)

1. Deploy do banco, API, Prometheus e Grafana:
```bash
kubectl apply -f k8s/base/staging
kubectl apply -f k8s/base/production
kubectl apply -f k8s/prometheus -R
kubectl apply -f k8s/grafana
```

2. Verificar pods e serviços:
```bash
kubectl get pods -n staging
kubectl get pods -n production
kubectl get svc -n staging
kubectl get svc -n production
```

3. Teste com IPs do LoadBalancer

http://<IP_STAGING>/converter?value=10&from=usd&to=brl \
http://<IP_PRODUCTION>/converter?value=20&from=usd&to=brl \
http://<IP_PRODUCTION>/history 

Mas se estiver rodando localmente, execute: \
`kubectl port-forward -n production svc/conversor 8080:80` \
`kubectl port-forward -n monitoring svc/prometheus 9090:9090` \
`kubectl port-forward -n monitoring svc/grafana 3000:3000`

## 4. Validando elasticidade (teste HPA)

### 4.1 Abra o monitoramento do HPA
`kubectl get hpa -n production -w`

### 4.2 Gere carga nos 2 pods existentes
`kubectl exec -it conversor-PODNAME -n production -- python -c "while True: 10**1000"`

No Grafana, você verá que o gráfico _CPU PER PODS_ vai subir e, como o HPA vai detectar o uso, você poderá ver o número de réplicas subindo tanto no terminal como no gráfico _NUMBER OF PODS_. _MEMORY_ vai ficar estável pois apenas CPU é requisitado.

## 5. Desafios e aprendizados

- Parâmetros do HPA: Grafana também foi usado para analisar o uso real da app e ajustar o HPA conforme à realidade.
- Service Discovery: implementação do Service Discovery para que novos pods sejam vistos automaticamente pelo Prometheus.
- Gerenciamento de secrets: Github bloqueou push de secrets. Recriar arquivos com placeholders é uma boa prática.
- Escopos no Docker Hub: push foi negado (insufficient scopes). Corrigido criando token com escopo de escrita.
- Contexto: Github não achava o path pois ainda não havia feito push a partir da raiz.
- Boas práticas CI/CD: deploy estava sem testes ou aprovação. É preciso validar primeiro o CI antes de prosseguir para CD.
- Kubeconfig: workflow falhava no job de produção (kubectl conectava no localhost). A variável KUBECONFIG foi definida em todos os jobs necessários.
- Portabilidade: substituir senhas, IPs, tokens por placeholders ou secrets, além de documentar o uso no README de forma clara.
- Dependências: Gunicorn não era encontrado pois não constava no requirements.txt.

## 6. Demonstração visual

📄 [CLIQUE AQUI para ver as imagens: p.1 - registro de conversões no banco; p.2- Alerta no Slack; p.3 - Alerta no Prometheus; p.4 - Jobs do Actions; p.5 - Gráficos no Grafana](docs/img.pdf)

Na p.5, perceba o HPA atuando: aumentando ou diminuindo o número de pods conforme o necessário.

### 7. CI/CD

O workflow (.github/workflows/ci-cd.yaml) é executado a cada push na branch main e realiza:
- Build e push da imagem Docker para o Docker Hub
- Deploy automático em ambiente Kubernetes de staging
- Deploy em produção (Digital Ocean) requer aprovação manual
- Testes automatizados em Python
 

### ✅ 8. Conclusão

Este projeto consolidou conhecimentos fundamentais para a atuação como DevOps Engineer, demonstrando a capacidade de arquitetar, automatizar e monitorar aplicações modernas em ambientes containerizados.