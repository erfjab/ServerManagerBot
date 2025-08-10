## **Setup**  

### **Server and Docker Setup**  

<details>
<summary>Show Server Commands</summary>

#### 1. Update the Server  
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Docker  
```bash
curl -fsSL https://get.docker.com | sh
```
</details>

---

### **Install & Run the Bot**  

<details>
<summary>Show Run Commands</summary>

#### 1. Create Directory and Download Files  
```bash
mkdir -p /opt/erfjab/servermanagerbot/data
curl -o /opt/erfjab/servermanagerbot/docker-compose.yml https://raw.githubusercontent.com/erfjab/servermanagerbot/master/docker-compose.yml
cd /opt/erfjab/servermanagerbot
curl -o .env https://raw.githubusercontent.com/erfjab/servermanagerbot/master/.env.example
nano .env
```

#### 2. Pull Docker Image  
```bash
docker compose pull
```

#### 3. Start the Bot  
```bash
docker compose up -d
```

After a few moments, the bot will start running.

</details>

---

### **Update the Bot**  

<details>
<summary>Show Update Commands</summary>

Make sure you're in the **servermanagerbot** directory:  
```bash
cd /opt/erfjab/servermanagerbot
```

Then update the bot:  
```bash
docker compose pull && docker compose up -d
```

</details>

---

### **Manage the Bot**  

<details>
<summary>Show Manage Commands</summary>

Make sure you're in the **servermanagerbot** directory:  
```bash
cd /opt/erfjab/servermanagerbot
```

- **Restart the Bot:**  
  ```bash
  docker compose restart
  ```

- **Stop the Bot:**  
  ```bash
  docker compose down
  ```

- **View Logs:**  
  ```bash
  docker compose logs -f
  ```

</details>

---

### **Switch to GA Mode (preview mode)**  

<details>
<summary>Show GA Commands</summary>

Make sure you're in the **HolderBot** directory:  
```bash
cd /opt/erfjab/servermanagerbot
```

- **Open the Docker Compose File:**  
  ```bash
  nano docker-compose.yml
  ```

- **Change the Image Tag:**  
  
  **From:**  
  ```yaml
  erfjab/servermanagerbot:latest
  ```
  **To:**  
  ```yaml
  erfjab/servermanagerbot:ga
  ```

- **Pull the Docker Image:**  
  ```bash
  docker compose pull
  ```

- **Start the Bot:**  
  ```bash
  docker compose up -d
  ```
</details>

---

## **Support**  

- **Telegram Channel:** [@ErfJabs](https://t.me/ErfJabs)  
- **Telegram Chat:** [@ErfJabChat](https://t.me/erfjabgroup)  

⭐ **Star the Project:**  
[![Stargazers](https://starchart.cc/erfjab/servermanagerbot.svg?variant=adaptive)](https://starchart.cc/erfjab/servermanagerbot)  