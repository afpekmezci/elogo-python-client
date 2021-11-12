class DocumentTypes:

    efatura = 'EINVOICE'
    efutara_zarf = 'ENVELOPE'
    efatura_zarfyanit = 'INVOICEAPPRESP'
    efatura_detay = 'EINVOICEDETAIL'
    earsiv_fatura = 'EARCHIVE'
    eirsaliye = 'DESPATCHADVICE'


    def get_param_string(self, fatura_type):
        return f"DOCUMENTTYPE={fatura_type}"