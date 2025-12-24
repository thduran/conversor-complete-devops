[Para PT-BR, clique aqui](#conversor-api---devops-end-to-end-portfólio)

# Converter - DevOps End-to-End (Portfolio)

## 1. About the project


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

Crie a secret pro Postgres:

```bash
# Staging
kubectl create secret generic db-admin-pass \
  --from-literal=PASSWORD="my-password" \
  -n staging

# Production
kubectl create secret generic db-admin-pass \
  --from-literal=PASSWORD="my-password" \
  -n production
```

Crie a secret para a aplicação:

```bash
# Staging
kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL="postgresql://postgres:my-password@postgres-svc:5432/app_db" \
  -n staging

# Production
kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL="postgresql://postgres:my-password@postgres-svc:5432/app_db" \
  -n production
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

- Quais números colocar no HPA -> o Grafana foi utilizado para ajustar os parâmetros do HPA conforme à realidade da aplicação.
- Prometheus não enxerga novos pods -> implementação do Service Discovery para que novos pods sejam vistos automaticamente.
- Github bloqueou push de secrets -> recriar arquivos com placeholders é uma boa prática
- Push no Docker Hub negado (insufficient scopes) -> corrigido criando token com escopo de escrita.
- Github não encontra path -> não havia feito push a partir da raiz
- Deploy sem testes nem aprovação -> validar primeiro o CI antes de expandir para CD.
- Workflow falhava no job de produção (kubectl conectava em localhost:8080) -> definir variável KUBECONFIG em todos os jobs necessários
- Tornar o projeto portável -> substituir todos os valores reais de senhas, IPs, tokens por placeholders ou secrets, além de documentar o uso no README de forma clara.
- Gunicorn não encontrado -> dependências precisam estar nos requirements.txt para serem "vistas"

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