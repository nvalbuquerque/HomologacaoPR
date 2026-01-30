' Alt + F11: Abre Microsoft VBA > Inserir > Módulo || Arquivo > Importar Arquivo... (.bas)
' Criar botão: aba Desenvolvedor > Inserir > Botao

Attribute VB_Name = "Módulo1"
Sub ClassificarDensidadeNuvem()

    Dim wbBase As Workbook
    Dim wsBase As Worksheet
    Dim wsResultado As Worksheet
    Dim dict As Object

    Dim ultimaLinhaBase As Long
    Dim ultimaLinhaResultado As Long
    Dim i As Long

    Dim nomeArquivo As String
    Dim densidade As Double

    ' === AJUSTE O CAMINHO DO ARQUIVO BASE ===
    Set wbBase = Workbooks.Open("E:\Homologacao_Nathalia\Testes\LAS_BE06.xlsx")
    Set wsBase = wbBase.Sheets("Planilha1")
    Set wsResultado = ThisWorkbook.Sheets("NPC")

    Set dict = CreateObject("Scripting.Dictionary")

    ' === LÊ A BASE E GUARDA EM MEMÓRIA ===
    ultimaLinhaBase = wsBase.Cells(wsBase.Rows.Count, "C").End(xlUp).Row

    For i = 2 To ultimaLinhaBase
        nomeArquivo = Trim(wsBase.Cells(i, "C").Value)
        densidade = wsBase.Cells(i, "Z").Value

        If nomeArquivo <> "" Then
            dict(nomeArquivo) = densidade
        End If
    Next i

    ' === PROCESSA O RESULTADO ===
    ultimaLinhaResultado = wsResultado.Cells(wsResultado.Rows.Count, "A").End(xlUp).Row

    For i = 17 To ultimaLinhaResultado
        nomeArquivo = Trim(wsResultado.Cells(i, "A").Value)

        If dict.exists(nomeArquivo) Then
            If dict(nomeArquivo) >= 4 Then
                wsResultado.Cells(i, "G").Value = "A"
            Else
                wsResultado.Cells(i, "G").Value = "AP"
            End If
        Else
            wsResultado.Cells(i, "G").Value = "Código inexistente"
        End If
    Next i

    wbBase.Close SaveChanges:=False

    MsgBox "Classificação concluída!", vbInformation

End Sub


