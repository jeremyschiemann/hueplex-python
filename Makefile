tailwind:
	./tailwind -i ./static/input.css -o ./static/output.css

tailwind-w:
	./tailwind -i ./static/input.css -o ./static/output.css -w -p

dl-tailwind:
	curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.1/tailwindcss-linux-x64
	mv ./tailwindcss-linux-x64 ./tailwind


server:
	poetry install
	HUE_KEY=VedQTM3d0McDdG7WapcajTtKE6F1kSY3qv3CYtIi poetry run uvicorn hueplex.server:app --reload