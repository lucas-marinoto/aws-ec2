# Informações de EC2 - VPC - SG e Rotas

**Principais Funcionalidades**

- Trazer todas as instâncias ativas do região que esta configurada o AWS Configure na máquina que esta executando
- Trazer informações de Security Group associado a EC2
- Trazer as Rotas criadas para a VPC da EC2
- Trazer as Associações de Rotas e Subnets
- Exporta todas as informações para um arquivo Excel na próprio caminho que esta executando. Arquivo Ec2.xlsx

#TODO

- Trazer os Security Groups com regras de Inbound e Outbound
- Testar quando tem mais de uma VPC na mesma regição

#Como executar

- Recomendado criar um ambiente virtual para o Python antes (opcional)
- Abrir a pasta do código e executar o comando abaixo para instalar as dependências

```pip install -r requirements.txt```

- Executar o programa e aguardar um print com a mensagem FIM
