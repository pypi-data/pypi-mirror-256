
from dotenv import load_dotenv
from sap_nota_pedido.session import sessionable
from SapGuiLibrary import SapGuiLibrary
# from robot.api import logger
import logging
import re

logger = logging.getLogger(__name__)
class NotaPedidoTransaction(SapGuiLibrary):
    def __init__(self) -> None:
        load_dotenv()
        pass

    @sessionable
    def execute(self, nota_pedido):
        logger.info(f"enter execute nota_pedido:{nota_pedido}")
        self.run_transaction('/nme21n')

        self.send_vkey(0)

        # REORGANIZA ELEMENTOS PARA GARANTIR QUE CABEÇALHO ESTEJA ABERTO
        self.send_vkey(29) # Fechar Cabeçalho
        self.send_vkey(30) # Fechar Síntese de itens
        self.send_vkey(31) # Fechar Detahe de item
        self.send_vkey(26) # Abrir Cabeçalho

        # PREENCHE DADOS INICIAIS (Antes do cabeçalho)
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB0:SAPLMEGUI:0030/subSUB1:SAPLMEGUI:1105/cmbMEPO_TOPLINE-BSART").Key = nota_pedido['tipo'] # Define o tipo de pedido como Ped.C.Custo/Ordem
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB0:SAPLMEGUI:0030/subSUB1:SAPLMEGUI:1105/ctxtMEPO_TOPLINE-SUPERFIELD").Text = nota_pedido['fornecedor']['codigo'] # Fornecedor

        # CABEÇALHO | Aba Dados Organizacionais
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB1:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1102/tabsHEADER_DETAIL/tabpTABHDT9").Select() #Seleciona a aba Dados organizacionais
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB1:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1102/tabsHEADER_DETAIL/tabpTABHDT9/ssubTABSTRIPCONTROL2SUB:SAPLMEGUI:1221/ctxtMEPO1222-EKORG").Text = nota_pedido['org_compras'] #orgCompras
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB1:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1102/tabsHEADER_DETAIL/tabpTABHDT9/ssubTABSTRIPCONTROL2SUB:SAPLMEGUI:1221/ctxtMEPO1222-EKGRP").Text = nota_pedido['grp_compradores'] #grpCompradores '(Constante: S01)
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0013/subSUB1:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1102/tabsHEADER_DETAIL/tabpTABHDT9/ssubTABSTRIPCONTROL2SUB:SAPLMEGUI:1221/ctxtMEPO1222-BUKRS").Text = nota_pedido['empresa'] #empresa '(Constante: HFNT)
        # Application.Wait Now + #12:00:02 AM# '(Avaliar a necessidade de inserir espera)

        # REORGANIZA ELEMENTOS PARA GARANTIR QUE SÍNTESE DE ITENS ESTEJA ABERTO
        self.send_vkey(29) #Fechar cabeçalho
        self.send_vkey(27) #Abrir Síntese de itens
        self.send_vkey(31) #Fechar Detahe de item
        self.send_vkey(26) #Abrir Cabeçalho
        self.send_vkey(29) #Fechar cabeçalho


        # SÍNTESE DE ITENS

        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0016/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-KNTTP[2,0]").Text = nota_pedido['sintese_de_itens'][0]['categoria_cc'] #categoriaCC '(Constante: K)
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0016/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-EMATN[4,0]").Text = nota_pedido['sintese_de_itens'][0]['material']['codigo']  # material
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0016/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/txtMEPO1211-MENGE[6,0]").Text = nota_pedido['sintese_de_itens'][0]['quantidade'] #quantidade
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0016/subSUB2:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1211/tblSAPLMEGUITC_1211/ctxtMEPO1211-NAME1[10,0]").Text = nota_pedido['sintese_de_itens'][0]['item']['cc']['centro'] #centro 'Local de negócio
        self.send_vkey(0)


        # DETALHES DE ITEM | Aba C|C

        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0019/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT13").Select() #Seleciona a aba C|C
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0019/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT13/ssubTABSTRIPCONTROL1SUB:SAPLMEVIEWS:1101/subSUB2:SAPLMEACCTVI:0100/subSUB1:SAPLMEACCTVI:1100/subKONTBLOCK:SAPLKACB:1101/ctxtCOBL-KOSTL").Text = nota_pedido['sintese_de_itens'][0]['item']['cc']['centro_custo'] #centroCusto
        self.send_vkey(0)
        self.send_vkey(0)
        self.send_vkey(0)


        # DETALHES DE ITEM | Aba Fatura

        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0019/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT7").Select() #Seleciona a aba fatura
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0015/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT7/ssubTABSTRIPCONTROL1SUB:SAPLMEGUI:1317/ctxtMEPO1317-MWSKZ").Text = nota_pedido['sintese_de_itens'][0]['item']['fatura']['codigo_imposto'] #codigoImposto #Inclui o código do imposto
        self.send_vkey(0 )


        # DETALHES DE ITEM | Aba Condições

        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0015/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT8").Select() #Seleciona a aba Condições
        self.session.findById("wnd[0]/usr/subSUB0:SAPLMEGUI:0019/subSUB3:SAPLMEVIEWS:1100/subSUB2:SAPLMEVIEWS:1200/subSUB1:SAPLMEGUI:1301/subSUB2:SAPLMEGUI:1303/tabsITEM_DETAIL/tabpTABIDT8/ssubTABSTRIPCONTROL1SUB:SAPLMEGUI:1333/ssubSUB0:SAPLV69A:6201/tblSAPLV69ATCTRL_KONDITIONEN/txtKOMV-KBETR[3,1]").Text = nota_pedido['sintese_de_itens'][0]['item']['condicoes']['valor_bruto'] #valorItem 'Valor bruto
        self.send_vkey(0 )



        # PROCESSO PARA ANEXAR O DOCUMENTO NO PEDIDO
        self.session.findById("wnd[0]/titl/shellcont/shell").pressButton("%GOS_TOOLBOX")
        self.session.findById("wnd[0]/shellcont[1]/shell").pressContextButton("CREATE_ATTA")
        self.session.findById("wnd[0]/shellcont[1]/shell").selectContextMenuItem("PCATTA_CREA")
        self.session.findById("wnd[1]/usr/ctxtDY_PATH").Text = nota_pedido['anexo']['path_dir'] #Diretório de NFs
        self.session.findById("wnd[1]/usr/ctxtDY_FILENAME").Text = nota_pedido['anexo']['filename'] #PDF da DANFE
        self.session.findById("wnd[1]/tbar[0]/btn[0]").press()

        self.session.findById("wnd[0]/tbar[0]/btn[11]").press() #'Grava o lançamento

        cod_nota_pedido = self._get_cod_nota_pedido()
        logger.info(f"Leave execute código da nota_pedido:{cod_nota_pedido}")
        return cod_nota_pedido

    def _get_cod_nota_pedido(self):
        cod_nota_pedido_msg = self.session.findById("wnd[0]/sbar").Text
        pattern ="^Ped.C.Custo\\/Ordem criado sob o nº ([0-9]{10,11})$"
        regex = re.compile(pattern , re.IGNORECASE)
        cod_nota_pedido_list = regex.search(cod_nota_pedido_msg)
        cod_nota_pedido = cod_nota_pedido_list[1]
        logger.info(f"Extracted cod_nota_pedido: '{cod_nota_pedido}', from: '{cod_nota_pedido_msg}'")
        return cod_nota_pedido