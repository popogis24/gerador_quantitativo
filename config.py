import os
from dynaconf import Dynaconf

# Obter o caminho absoluto para o arquivo settings.toml
settings_file_path = os.path.join(os.path.dirname(__file__), 'settings.toml')

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        settings_file_path,
        # Adicione outros arquivos de configuração, se necessário
    ],
)