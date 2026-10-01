
Traefik command arg conf for auto tls and my defaults
```yaml
command:
  # Dashboard & logging
  - "--api.insecure=false"
  - "--api.dashboard=true"
  - "--log.level=INFO"

  # Docker provider
  - "--providers.docker=true"
  - "--providers.docker.exposedbydefault=false"
  - "--providers.docker.network=homelab"

  # HTTP & HTTPS entrypoints
  - "--entryPoints.web.address=:80"
  - "--entryPoints.websecure.address=:443"

  # Enable TLS on HTTPS
  - "--entryPoints.websecure.http.tls=true"

  # Redirect HTTP → HTTPS
  - "--entryPoints.web.http.redirections.entryPoint.to=websecure"
  - "--entryPoints.web.http.redirections.entryPoint.scheme=https"

  # Let's Encrypt / ACME
  - "--certificatesresolvers.le.acme.email=${DOMAIN_EMAIL}"
  - "--certificatesresolvers.le.acme.storage=/letsencrypt/acme.json"
  - "--certificatesresolvers.le.acme.httpchallenge.entrypoint=web"
```


Label template for traefik and homepage autodiscovery
``` yaml
# Traefik labels
- "traefik.enable=true"
- "traefik.http.routers.<SERVICE>.rule=Host(`<SERVICE>.${DOMAIN}`)"
- "traefik.http.routers.<SERVICE>.entrypoints=web,websecure"
- "traefik.http.routers.<SERVICE>.tls=true"
- "traefik.http.routers.<SERVICE>.tls.certresolver=le"
- "traefik.http.services.<SERVICE>.loadbalancer.server.port=<PORT>"

# Homepage labels
- "homepage.group=<GROUP>"
- "homepage.name=<NAME>"
- "homepage.icon=<ICON>"
- "homepage.href=https://<SERVICE>.$DOMAIN/"
- "homepage.description=<DESCRIPTION>"
```