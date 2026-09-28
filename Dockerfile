FROM python:3.12-slim

WORKDIR /app
COPY persistent_auditor.py .

# Inventory is stored in /data so it can be mounted as a volume
ENV INVENTORY_PATH=/data/inventory.txt

CMD ["python", "persistent_auditor.py"]
