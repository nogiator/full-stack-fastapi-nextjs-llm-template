Traefik na produkcji:

service powinien być opcjonalny
dodatkowo labels pod traefik powinny być opcjonalne
Ale mamy tu 3 sytuacje.

używamy czegoś innego
używamy swojego Traefik spoza projektu
używamy tego co dostarczyłeś i tylko ten scenariusz mamy obsłużony
Kończąc wątek Traefika wpisy typu: traefik.http.routers.api.rule muszą być unikalne na poziomie serwera. Konkretnie api ma być unikalne.

.env - proponuję generowanie tego pliku
docker-compose.prod.yml idzie do repozytorium. Chyba nie chcemy by user przez nieuwagę wysłał do repo credentials do bazy danych.
Dodatkowo załatwi to nam powyższy problem z unikalnością labels dla Traefik.
Przykładowo: traefik.http.routers.api-${CONTAINER_NAME}.rule

W .env dajemy:
CONTAINER_NAME=project_name
BACKEND_URL=https://project_name.com

Dodatkowo jeśli mamy:

"traefik.http.services.frontend.loadbalancer.server.port={{ cookiecutter.frontend_port }}"
to w przypadku portów 80 i 443 nie podajemy tego bo nie ma sensu. Traefik automatycznie działa na tych portach.

O i kolejne znalezisko:
- BACKEND_URL=http://app:{{ cookiecutter.backend_port }}
po pierwsze czy to zadziała? Przecież podajesz wewnętrzny host w tej sieci dockera.

Ale wyszedł PR przez Mattermosta :)

