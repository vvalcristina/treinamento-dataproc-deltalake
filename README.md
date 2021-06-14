# Treinamento Dataproc e DeltaLake

Este repositório tem o objetivo de prover um ambiente de treinamento da integração do [Delta Lake](https://docs.delta.io/latest/index.html) no GCP com o [Dataproc](https://cloud.google.com/dataproc/docs).

### Pré-requisitos de execução:

* Para a execução do Delta Lake e o ambiente do GCP é necessária a utilização do Spark na versão 3.0.0 e o Delta Lake em sua versão 0.8.

* Certifique-se que a SDK do Gcloud está instalado no seu PC. Se não, siga as [instruções da documentação](https://cloud.google.com/sdk/docs/install) conforme seu Sistema Operacional.
### Estrutura do repositório:

```shell
    ├── images                      -> Images setup
    ├── jobs 
        ├── job_deltalake.py        -> Job de merge de 2 dataframes no GCloud Storage
    ├── scripts
        ├── deploy_run              -> Script de deploy do código no Gcloud Storage
        ├── init_actions            -> Script de ações de setup do Dataproc
        ├── load_env                -> Script de export de variáveis de ambiente
    ├── workflow
        ├── workflow.yaml           -> Workflow template do Dataproc com DeltaLake
    ├── .gitignore                  -> .gitignore
    ├── HandsOn DeltaLake.ipynb     -> Notebook de exploração do deltalake e criação dos dataframes para exploração
    ├── README.md                   -> README.md 
    ├── requirements.txt            -> Libs necessarias para execução
    ├── setup.py                    -> setup.py
```

### Como rodar esse projeto:

* Faça um git clone do projeto.

* Execute o notebook [*HandsOn DeltaLake.ipynb*](HandsOn%20DeltaLake.ipynb) para entender um pouco do funcionamento do Delta Lake e entendimento de execução do processo de merge de 2 datasets.

* Para executar esse código no Dataproc substitua o PROJECT_ID e o BUCKET_CODE_NAME para o nome do seu projeto e do seu bucket que armazena o código no ambiente do Gcloud no script [*env*](scripts/env).

* Substitua o nome do BUCKET_CODE_NAME no arquivo [*workflow.yaml*](workflow/workflow.yaml).

* Para rodar o projeto no GCP, certifique-se que há a pasta *data/input/* não se encontra vazia. Os dataframes para teste podem ser criados através do Notebook.

```
    cd treinamento-dataproc-deltalake/scripts/
    bash ./deploy_run
```
