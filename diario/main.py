from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from .models import Entidade, Convenio, Lancamentos, HistoricosPadrao, PlanoContas
from . import db
import datetime

data_e_hora_atuais = datetime.datetime.now()
data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/entidade')
@login_required
def entidade():
    return render_template('entidade.html', name=current_user.name)


@main.route('/entidade', methods=['GET', 'POST'])
@login_required
def entidade_post():
    if request.method == 'POST':
        nome_entidade = request.form.get('nome_entidade')
        cnpj = request.form.get('cnpj')
        rua = request.form.get('rua')
        numero = request.form.get('numero')
        bairro = request.form.get('bairro')
        cep = request.form.get('cep')
        cidade = request.form.get('cidade')
        estado = request.form.get('estado')
        email = request.form.get('email')
        telefone = request.form.get('telefone')

        # cadastra uma nova entidade.
        entidade = Entidade(nome_entidade=nome_entidade, cnpj=cnpj, rua=rua,
                            numero=numero, bairro=bairro, cep=cep,
                            cidade=cidade, estado=estado, email=email,
                            telefone=telefone)

        # adiciona uma nova entidade no database "diario" na tabela "entidade"
        db.session.add(entidade)
        db.session.commit()
        return redirect(url_for('main.entidade'))


@main.route('/convenio')
@login_required
def convenio():
    return render_template('convenio.html', name=current_user.name)


@main.route('/convenio', methods=['GET', 'POST'])
@login_required
def convenio_post():
    if request.method == 'POST':
        nome_convenio = request.form.get('nome_convenio')
        orgao_concessor = request.form.get('orgao_concessor')
        num_contrato = request.form.get('num_contrato')
        data_rec_recurso = request.form.get('data_rec_recurso')
        vr_total_convenio = request.form.get('vr_total_convenio')
        ano_exercicio = request.form.get('ano_exercicio')
        saldo_anterior = request.form.get('saldo_anterior')

        # cadastra um novo convenio.
        convenio = Convenio(nome_convenio=nome_convenio, orgao_concessor=orgao_concessor,
                            num_contrato=num_contrato, data_rec_recurso=data_rec_recurso,
                            vr_total_convenio=vr_total_convenio, ano_exercicio=ano_exercicio,
                            saldo_anterior=saldo_anterior)

        # adiciona um novo convenio no database "diario" na tabela "convenio"
        db.session.add(convenio)
        db.session.commit()
        return redirect(url_for('main.convenio'))


@main.route('/pagamentos')
@login_required
def pagamentos():
    plano_contas = PlanoContas.query.all()
    historicos_padrao = HistoricosPadrao.query.all()
    return render_template('pagamentos.html', name=current_user.name,
                           historicos_padrao=historicos_padrao, plano_contas=plano_contas)


@main.route('/pagamentos', methods=['GET', 'POST'])
@login_required
def pagamentos_post():
    if request.method == 'POST':
        data = request.form.get('data')
        cod1_conta_devedora = request.form.get('cod_acesso2')
        cod2_conta_devedora = request.form.get('classificador2')
        descricao_conta_devedora = request.form.get('nome_conta2')
        cod1_conta_credora = request.form.get('cod_acesso')
        cod2_conta_credora = request.form.get('classificador')
        descricao_conta_credora = request.form.get('nome_conta')
        nat_despesa = request.form.get('nat_despesa')
        cod_historico = request.form.get('codigohisto')
        descricao_historico = request.form.get('titulohisto')
        cpl_historico = request.form.get('cpl_historico')
        doc_deposito = request.form.get('doc_deposito')
        valor = request.form.get('valor')
        pagamento = request.form.get('pagamento')
        if '.' in valor:
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        if ',' in valor:
            valor = valor.replace(',', '.')
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        else:
            valor = float(valor)
            valor = "{:.2f}".format(valor)

        lancamentos = Lancamentos(data=data,
                                  cod1_conta_devedora=cod1_conta_devedora,
                                  cod2_conta_devedora=cod2_conta_devedora,
                                  descricao_conta_devedora=descricao_conta_devedora,
                                  cod1_conta_credora=cod1_conta_credora,
                                  cod2_conta_credora=cod2_conta_credora,
                                  descricao_conta_credora=descricao_conta_credora,
                                  nat_despesa=nat_despesa,
                                  cod_historico=cod_historico,
                                  descricao_historico=descricao_historico,
                                  cpl_historico=cpl_historico,
                                  doc_deposito=doc_deposito,
                                  valor=valor, pagamento=pagamento)
        # adiciona um novo pagamento no database "diario" na tabela "lancamentos"
        db.session.add(lancamentos)
        db.session.commit()
        return redirect(url_for('main.pagamentos'))


@main.route('/recebimentos')
@login_required
def recebimentos():
    plano_contas = PlanoContas.query.all()
    historicos_padrao = HistoricosPadrao.query.all()
    return render_template('recebimentos.html', name=current_user.name,
                           historicos_padrao=historicos_padrao, plano_contas=plano_contas)


@main.route('/recebimentos', methods=['GET', 'POST'])
@login_required
def recebimentos_post():
    if request.method == 'POST':
        data = request.form.get('data')
        cod1_conta_credora = request.form.get('cod_acesso2')
        cod2_conta_credora = request.form.get('classificador2')
        descricao_conta_credora = request.form.get('nome_conta2')
        cod1_conta_devedora = request.form.get('cod_acesso')
        cod2_conta_devedora = request.form.get('classificador')
        descricao_conta_devedora = request.form.get('nome_conta')
        cod_historico = request.form.get('codigohisto')
        descricao_historico = request.form.get('titulohisto')
        cpl_historico = request.form.get('cpl_historico')
        doc_deposito = request.form.get('doc_deposito')
        valor = request.form.get('valor')
        recebimento = request.form.get('recebimento')
        if '.' in valor:
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        if ',' in valor:
            valor = valor.replace(',', '.')
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        else:
            valor = float(valor)
            valor = "{:.2f}".format(valor)

        lancamentos = Lancamentos(data=data,
                                  cod1_conta_devedora=cod1_conta_devedora,
                                  cod2_conta_devedora=cod2_conta_devedora,
                                  descricao_conta_devedora=descricao_conta_devedora,
                                  cod1_conta_credora=cod1_conta_credora,
                                  cod2_conta_credora=cod2_conta_credora,
                                  descricao_conta_credora=descricao_conta_credora,
                                  cod_historico=cod_historico,
                                  descricao_historico=descricao_historico,
                                  cpl_historico=cpl_historico,
                                  doc_deposito=doc_deposito,
                                  valor=valor, recebimento=recebimento)
        # adiciona um novo pagamento no database "diario" na tabela "lancamentos"
        db.session.add(lancamentos)
        db.session.commit()
        return redirect(url_for('main.recebimentos'))


@main.route('/atualizarsaldos')
@login_required
def saldos():
    lancamentos = Lancamentos.query.all()
    for i in lancamentos:
        if i.descricao_conta_devedora == 'Caixa' and i.cpl_historico == 'Saldo Anterior':
            return render_template('saldos.html', name=current_user.name, lancamentos=lancamentos)
    return render_template('saldos.html', name=current_user.name, lancamentos=lancamentos)

@main.route('/atualizarsaldos', methods=['GET', 'POST'])
@login_required
def atualizarsaldos_post():
    if request.method == 'POST':
        data = request.form.get('data')
        descricao_conta_devedora = request.form.get('descricao_conta_devedora')
        descricao_conta_credora = request.form.get('descricao_conta_credora')
        descricao_historico = request.form.get('descricao_historico')
        cpl_historico = request.form.get('cpl_historico')
        valor = request.form.get('valor')
        recebimento = request.form.get('recebimento')
        if '.' in valor:
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        if ',' in valor:
            valor = valor.replace(',', '.')
            valor = float(valor)
            valor = "{:.2f}".format(valor)
        else:
            valor = float(valor)
            valor = "{:.2f}".format(valor)

        lancamentos = Lancamentos(data=data,
                                  descricao_conta_devedora=descricao_conta_devedora,
                                  descricao_conta_credora=descricao_conta_credora,
                                  descricao_historico=descricao_historico,
                                  valor=valor, cpl_historico=cpl_historico, recebimento=recebimento)
        # adiciona um novo pagamento no database "diario" na tabela "lancamentos"
        db.session.add(lancamentos)
        db.session.commit()
        return redirect(url_for('main.atualizarsaldos_post'))


# abre a tela para seleção de relatórios"
@main.route('/sel_relatorio1')
@login_required
def sel_relatorio1():
    plano_contas = PlanoContas.query.all()
    return render_template('sel_relatorio1.html', name=current_user.name, plano_contas=plano_contas)


@main.route('/sel_relatorio1', methods=['GET', 'POST'])
def sel_relatorio1_post():
    global recurso, recurso2, ano, mes, data_e_hora_em_texto, soma1, soma2, tot1, tot2
    lancamentos = Lancamentos.query.all()
    soma1 = 0
    tot1 = 0

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')
        recurso = request.form.get('recurso')
        recurso2 = request.form.get('recurso2')

    for i in lancamentos:
        if ano == i.data[0:4] and mes == i.data[5:7] and recurso2 == i.descricao_conta_credora[0:30]:
            x = float(i.valor)
            soma1 += x
            tot1 += 1


    soma2 = 0
    tot2 = 0

    for i in lancamentos:
        if ano == i.data[0:4] and mes == i.data[5:7] and recurso == i.descricao_conta_credora[0:30]:
            x = float(i.valor)
            soma2 += x
            tot2 += 1
    convenio = Convenio.query.all()
    entidade = Entidade.query.all()

    return render_template('relatorio1.html', name=current_user.name, recurso=recurso,
                           recurso2=recurso2, ano=ano, mes=mes, convenio=convenio, entidade=entidade,
                           data_e_hora_em_texto=data_e_hora_em_texto, lancamentos=lancamentos,
                           soma1=soma1, soma2=soma2, tot1=tot1, tot2=tot2)


@main.route('/relatorio1', methods=['GET', 'POST'])
@login_required
def relatorio1():
    return render_template('relatorio1.html', name=current_user.name)


@main.route('/sel_relatorio2')
@login_required
def sel_relatorio2():
    plano_contas = PlanoContas.query.all()
    return render_template('sel_relatorio2.html', name=current_user.name, plano_contas=plano_contas)


@main.route('/sel_relatorio2', methods=['GET', 'POST'])
def sel_relatorio2_post():
    global recurso, ano, mes, data_e_hora_em_texto, soma1, soma2, tot1, tot2
    lancamentos = Lancamentos.query.all()
    soma1 = 0
    tot1 = 0

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')
        recurso = request.form.get('recurso')

    for i in lancamentos:
        if ano == i.data[0:4] and mes == i.data[5:7] and recurso == i.descricao_conta_credora[0:5]:
            x = float(i.valor)
            soma1 += x
            tot1 += 1


    soma2 = 0
    tot2 = 0
    for i in lancamentos:
        if ano == i.data[0:4] and mes == i.data[5:7] and recurso == i.descricao_conta_devedora[0:5]:
            x = float(i.valor)
            soma2 += x
            tot2 += 1

    convenio = Convenio.query.all()
    entidade = Entidade.query.all()

    return render_template('relatorio2.html', name=current_user.name, lancamentos=lancamentos,
                           recurso=recurso, ano=ano, mes=mes, convenio=convenio, entidade=entidade,
                           data_e_hora_em_texto=data_e_hora_em_texto,
                           soma1=soma1, soma2=soma2, tot1=tot1, tot2=tot2)


@main.route('/relatorio2', methods=['GET', 'POST'])
@login_required
def relatorio2():
    return render_template('relatorio2.html', name=current_user.name)


 # abre a tela para seleção consulta lançamentos de pagamentos e recebimentos
@main.route('/sel_consulta1')
@login_required
def sel_consulta1():
    return render_template('sel_consulta1.html', name=current_user.name)


@main.route('/sel_consulta1', methods=['GET', 'POST'])
def consultas_pagamentos():
    global ano, mes, soma1
    lancamentos = Lancamentos.query.all()
    soma1 = 0

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')

    for i in lancamentos:
        if ano == i.data[0:4] and mes == i.data[5:7] and i.pagamento == 'p':
            x = float(i.valor)
            soma1 += x

    return render_template('consulta1.html', name=current_user.name, lancamentos=lancamentos,
                           ano=ano, mes=mes, soma1=soma1)


@main.route('/consulta1')  # renderiza o formulario da consulta de pagamentos
@login_required
def consulta1():
    return render_template('consulta1.html', name=current_user.name)


@main.route('/sel_consulta2')
@login_required
def sel_consulta2():
    return render_template('sel_consulta2.html', name=current_user.name)


@main.route('/sel_consulta2', methods=['GET', 'POST'])
def consultas_recebimentos():
    global ano, mes, soma2
    lancamentos = Lancamentos.query.all()
    soma2 = 0

    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')

    for i in lancamentos:
        if ano == i.data[0:4] and mes == i.data[5:7] and i.recebimento == 'r':
            x = float(i.valor)
            soma2 += x

    return render_template('consulta2.html', name=current_user.name, lancamentos=lancamentos,
                           ano=ano, mes=mes, soma2=soma2)


@main.route('/consulta2')  # renderiza o formulario da consulta de recebimentos
@login_required
def consulta2():
    return render_template('consulta2.html', name=current_user.name)


@main.route('/consulta3')  # consulta a entidade
@login_required
def consulta3():
    entidade = Entidade.query.all()
    return render_template('consulta3.html', name=current_user.name, entidade=entidade)


@main.route('/consulta4')  # consulta o convenio
@login_required
def consulta4():
    convenio = Convenio.query.all()
    return render_template('consulta4.html', name=current_user.name, convenio=convenio)


@main.route('/sel_exportar1')
@login_required
def sel_exportar1():
    return render_template('sel_exportar1.html', name=current_user.name)


@main.route('/sel_exportar1', methods=['GET', 'POST'])
def exportar_dados1():
    global ano, mes
    lancamentos = Lancamentos.query.all()
    if request.method == 'POST':
        mes = request.form.get('mes')
        ano = request.form.get('ano')

    return render_template('exportar1.html', name=current_user.name, lancamentos=lancamentos,
                           ano=ano, mes=mes)


@main.route("/excluir1/<int:id>", methods=['GET', 'POST'])
@login_required
def excluir1(id):
    lancamentos = Lancamentos.query.filter_by(id=id).first()
    if request.method == 'POST':
        if lancamentos:
            db.session.delete(lancamentos)
            db.session.commit()
            return redirect(url_for('main.sel_consulta1'))
    return render_template('delete.html')


@main.route("/excluir2/<int:id>", methods=['GET', 'POST'])
@login_required
def excluir2(id):
    lancamentos = Lancamentos.query.filter_by(id=id).first()
    if request.method == 'POST':
        if lancamentos:
            db.session.delete(lancamentos)
            db.session.commit()
            return redirect(url_for('main.sel_consulta2'))
    return render_template('delete.html')


@main.route("/excluir3/<int:id>", methods=['GET', 'POST'])
@login_required
def excluir3(id):
    entidade = Entidade.query.filter_by(id=id).first()
    if request.method == 'POST':
        if entidade:
            db.session.delete(entidade)
            db.session.commit()
            return redirect(url_for('main.consulta3'))
    return render_template('delete.html')


@main.route("/excluir4/<int:id>", methods=['GET', 'POST'])
@login_required
def excluir4(id):
    convenio = Convenio.query.filter_by(id=id).first()
    if request.method == 'POST':
        if convenio:
            db.session.delete(convenio)
            db.session.commit()
            return redirect(url_for('main.consulta4'))
    return render_template('delete.html')


@main.route("/atualizar1/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar1(id):
    lancamentos = Lancamentos.query.filter_by(id=id).first()
    plano_contas = PlanoContas.query.all()
    historicos_padrao = HistoricosPadrao.query.all()
    if request.method == 'POST':
        if lancamentos:
            db.session.delete(lancamentos)
            db.session.commit()

            data = request.form.get('data')
            cod1_conta_devedora = request.form.get('cod_acesso2')
            cod2_conta_devedora = request.form.get('classificador2')
            descricao_conta_devedora = request.form.get('nome_conta2')
            cod1_conta_credora = request.form.get('cod_acesso')
            cod2_conta_credora = request.form.get('classificador')
            descricao_conta_credora = request.form.get('nome_conta')
            nat_despesa = request.form.get('nat_despesa')
            cod_historico = request.form.get('codigohisto')
            descricao_historico = request.form.get('titulohisto')
            cpl_historico = request.form.get('cpl_historico')
            doc_deposito = request.form.get('doc_deposito')
            valor = request.form.get('valor')
            pagamento = request.form.get('pagamento')
            if '.' in valor:
                valor = float(valor)
                valor = "{:.2f}".format(valor)
            if ',' in valor:
                valor = valor.replace(',', '.')
                valor = float(valor)
                valor = "{:.2f}".format(valor)
            else:
                valor = float(valor)
                valor = "{:.2f}".format(valor)

            # atualiza um pagamento.
            lancamentos = Lancamentos(data=data,
                                      cod1_conta_devedora=cod1_conta_devedora,
                                      cod2_conta_devedora=cod2_conta_devedora,
                                      descricao_conta_devedora=descricao_conta_devedora,
                                      cod1_conta_credora=cod1_conta_credora,
                                      cod2_conta_credora=cod2_conta_credora,
                                      descricao_conta_credora=descricao_conta_credora,
                                      nat_despesa=nat_despesa,
                                      cod_historico=cod_historico,
                                      descricao_historico=descricao_historico,
                                      cpl_historico=cpl_historico,
                                      doc_deposito=doc_deposito,
                                      valor=valor, pagamento=pagamento)

            db.session.add(lancamentos)
            db.session.commit()
            return redirect(url_for('main.sel_consulta1'))

    return render_template('atualizar1.html', lancamentos=lancamentos,
                           historicos_padrao=historicos_padrao, plano_contas=plano_contas)


@main.route("/atualizar2/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar2(id):
    lancamentos = Lancamentos.query.filter_by(id=id).first()
    plano_contas = PlanoContas.query.all()
    historicos_padrao = HistoricosPadrao.query.all()
    if request.method == 'POST':
        if lancamentos:
            db.session.delete(lancamentos)
            db.session.commit()

            data = request.form.get('data')
            cod1_conta_devedora = request.form.get('cod_acesso')
            cod2_conta_devedora = request.form.get('classificador')
            descricao_conta_devedora = request.form.get('nome_conta')
            cod1_conta_credora = request.form.get('cod_acesso2')
            cod2_conta_credora = request.form.get('classificador2')
            descricao_conta_credora = request.form.get('nome_conta2')
            nat_despesa = request.form.get('nat_despesa')
            cod_historico = request.form.get('codigohisto')
            descricao_historico = request.form.get('titulohisto')
            cpl_historico = request.form.get('cpl_historico')
            doc_deposito = request.form.get('doc_deposito')
            valor = request.form.get('valor')
            recebimento = request.form.get('recebimento')
            if '.' in valor:
                valor = float(valor)
                valor = "{:.2f}".format(valor)
            if ',' in valor:
                valor = valor.replace(',', '.')
                valor = float(valor)
                valor = "{:.2f}".format(valor)
            else:
                valor = float(valor)
                valor = "{:.2f}".format(valor)

            # atualiza um recebimento.
            lancamentos = Lancamentos(data=data,
                                      cod1_conta_devedora=cod1_conta_devedora,
                                      cod2_conta_devedora=cod2_conta_devedora,
                                      descricao_conta_devedora=descricao_conta_devedora,
                                      cod1_conta_credora=cod1_conta_credora,
                                      cod2_conta_credora=cod2_conta_credora,
                                      descricao_conta_credora=descricao_conta_credora,
                                      nat_despesa=nat_despesa,
                                      cod_historico=cod_historico,
                                      descricao_historico=descricao_historico,
                                      cpl_historico=cpl_historico,
                                      doc_deposito=doc_deposito,
                                      valor=valor, precebimento=recebimento)

            db.session.add(lancamentos)
            db.session.commit()
            return redirect(url_for('main.sel_consulta2'))

    return render_template('atualizar2.html', lancamentos=lancamentos,
                           historicos_padrao=historicos_padrao, plano_contas=plano_contas)


@main.route("/atualizar3/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar3(id):
    entidade = Entidade.query.filter_by(id=id).first()
    if request.method == 'POST':
        if entidade:
            db.session.delete(entidade)
            db.session.commit()

            nome_entidade = request.form.get('nome_entidade')
            cnpj = request.form.get('cnpj')
            rua = request.form.get('rua')
            numero = request.form.get('numero')
            bairro = request.form.get('bairro')
            cep = request.form.get('cep')
            cidade = request.form.get('cidade')
            estado = request.form.get('estado')
            email = request.form.get('email')
            telefone = request.form.get('telefone')

        entidade = Entidade(nome_entidade=nome_entidade, cnpj=cnpj, rua=rua,
                            numero=numero, bairro=bairro, cep=cep,
                            cidade=cidade, estado=estado, email=email,
                            telefone=telefone)

        db.session.add(entidade)
        db.session.commit()
        return redirect(url_for('main.consulta3'))
    return render_template('atualizar3.html', entidade=entidade)


@main.route("/atualizar4/<int:id>", methods=['GET', 'POST'])
@login_required
def atualizar4(id):
    convenio = Convenio.query.filter_by(id=id).first()
    if request.method == 'POST':
        if convenio:
            db.session.delete(convenio)
            db.session.commit()

            nome_convenio = request.form.get('nome_convenio')
            orgao_concessor = request.form.get('orgao_concessor')
            num_contrato = request.form.get('num_contrato')
            data_rec_recurso = request.form.get('data_rec_recurso')
            vr_total_convenio = request.form.get('vr_total_convenio')
            ano_exercicio = request.form.get('ano_exercicio')
            saldo_anterior = request.form.get('saldo_anterior')

            convenio = Convenio(nome_convenio=nome_convenio, orgao_concessor=orgao_concessor,
                                num_contrato=num_contrato, data_rec_recurso=data_rec_recurso,
                                vr_total_convenio=vr_total_convenio, ano_exercicio=ano_exercicio,
                                saldo_anterior=saldo_anterior)

            db.session.add(convenio)
            db.session.commit()
            return redirect(url_for('main.consulta4'))
    return render_template('atualizar4.html', convenio=convenio)
