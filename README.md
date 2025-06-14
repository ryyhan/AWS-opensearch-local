# Setting Up a Persistent Local Instance of AWS OpenSearch Using Docker

This guide walks you through creating a **persistent local instance** of AWS OpenSearch with **Docker** and **Docker Compose**. Follow these step-by-step instructions to get your OpenSearch environment up and running.

---

## Prerequisites

* A Linux machine (tested on Ubuntu)
* `curl` installed
* Basic understanding of Docker

---

## Step 1: Install Docker (If Not Installed)

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable docker
sudo systemctl start docker
```

### Add Your User to Docker Group (Optional but Recommended)

```bash
sudo usermod -aG docker $USER
newgrp docker
```

---

## Step 2: Install Docker Compose (If Not Installed)

Check version:

```bash
docker-compose --version
```

If not available:

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
-o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```

---

## Step 3: Create Docker Compose File

Create a file named `docker-compose.yml` and add the following configuration:

```yaml
version: "3.9"

services:
  opensearch:
    image: public.ecr.aws/opensearchproject/opensearch:3
    container_name: opensearch
    environment:
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=Test@123
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - opensearch-data:/usr/share/opensearch/data
    ports:
      - 9200:9200
      - 9600:9600

  opensearch-dashboards:
    image: public.ecr.aws/opensearchproject/opensearch-dashboards:3
    container_name: opensearch-dashboards
    ports:
      - 5601:5601
    environment:
      - OPENSEARCH_HOSTS=https://opensearch:9200
      - OPENSEARCH_USERNAME=admin
      - OPENSEARCH_PASSWORD=Test@123
      - SERVER_SSL_ENABLED=false
    depends_on:
      - opensearch

volumes:
  opensearch-data:
```

---

## Step 4: Running OpenSearch Locally

### Start the Containers

```bash
docker-compose up -d
```

### Stop the Containers

```bash
docker-compose down
```

---

## Step 5: Access OpenSearch

* **OpenSearch API Endpoint:** [https://localhost:9200](https://localhost:9200)
* **OpenSearch Dashboards:** [http://localhost:5601](http://localhost:5601)

### Default Credentials:

* **Username:** `admin`
* **Password:** `Test@123`

---

## Screenshots

### ✅ OpenSearch API Running at `localhost:9200`

![Screenshot from 2025-06-13 19-54-03](https://github.com/user-attachments/assets/3907b485-a6a2-4437-a1e3-e0778ddd78d1)


### 📊 OpenSearch Dashboards at `localhost:5601`

![Screenshot from 2025-06-13 19-49-59](https://github.com/user-attachments/assets/56b89841-3185-46e1-8664-2a5c1b59c78c)


### 🐍 Sample Python Script Output

![Screenshot from 2025-06-14 11-58-55](https://github.com/user-attachments/assets/e6755cdb-712f-4739-8a3c-ab0e5e444e99)


---

## Step 6: Sample Python Script (Optional)

Attached in this repository, look for file localOpensearchTest.py

---

## Conclusion

You now have a **persistent local instance** of AWS OpenSearch with a **dashboard interface** and can connect to it via Python or any preferred client.

> ⚠️ **Note:** This setup is for **local development only**. For production, security and configurations need hardening.

---

