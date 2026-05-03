# Intentionally insecure Dockerfile for BreachLens IaC scanner (Checkov)
# DO NOT BUILD — every line here exists to trigger a known check.

# CKV_DOCKER_7: Use a specific tag, not :latest
FROM node:14

# CKV_DOCKER_3: Should NOT install packages without --no-install-recommends
# CKV_DOCKER_9: Should pin apt package versions
RUN apt-get update && apt-get install -y curl wget vim

# CKV_DOCKER_4: Use COPY instead of ADD
ADD . /app

WORKDIR /app

# CKV_DOCKER_5: Don't expose secret env vars
ENV DATABASE_PASSWORD=hunter2_PROD_secret
ENV API_KEY=sk_live_4eC39HqLyjWDarjtT1zdp7dc

# CKV_DOCKER_1: Should NOT expose port 22 (SSH)
EXPOSE 22 80 3000

# CKV_DOCKER_2: Should have a HEALTHCHECK instruction (missing — Checkov flags absence)

# CKV_DOCKER_8: Should NOT run as root user
USER root

CMD ["node", "vulnerable.js"]
