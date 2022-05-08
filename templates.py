# -*- coding: utf-8 -*-

from string import Template


class MiTemplate(Template):
    """
    Sobreescribe Template para crear la función substituye
    que convierte False/True en false/true para json.loads
    """
    def substituye(self, *args, **kws):
        if args:
            dct = args[0]
            for k, v in dct.items():
                if type(v) == bool:
                    dct[k] = str(v).lower()
        return self.substitute(*args, **kws)


emisor_factura = """{
    "razonSocialONombre": "$razonSocialONombre",
    "apellido1": "$apellido1",
    "apellido2": "$apellido2",
    "nif": "$nif",
    "codigoPostal": "$codigoPostal"
}"""

destinatario_factura_extranjero = """{
    "pais": "$pais",
    "identificacion": "$identificacion",
    "claveIdentificacionPaísResidencia": "$claveIdentificacionPaísResidencia"
}"""

destinatario_factura = """{
    "razonSocialONombreApellidos": "$razonSocialONombreApellidos",
    "nif": "$nif",
    "codigoPostal": "$codigoPostal",
    "direccion": "$direccion",
    "municipio": "$municipio",
    "destinatarioExtranjero": $destinatarioExtranjero
}"""

linea_factura = """{
    "tipoLineaContraparteNoNacional": "$tipoLineaContraparteNoNacional",
    "tipoSujecion": "$tipoSujecion",
    "causaExencionSujecionYNoSujecion": "$causaExencionSujecionYNoSujecion",
    "concepto": "$concepto",
    "precioUnitario": $precioUnitario,
    "cantidad": $cantidad,
    "descuentoSobreBaseImponible": $descuentoSobreBaseImponible,
    "porcentajeIva": $porcentajeIva,
    "recargoEquivalencia": $recargoEquivalencia,
    "porcentajeRetencion": $porcentajeRetencion,
    "claveIVA": "$claveIVA"
}"""

factura = """{
    "produccion": $produccion,
    "descripcion": "$descripcion",
    "fechaOperacion": "$fechaOperacion",
    "fechaExpedicion": "$fechaExpedicion",
    "serie": "$serie",
    "numeroFactura": $numeroFactura,
    "simplificada": $simplificada,
    "emisor": $emisor,
    "destinatario": $destinatario,  
    "lineasFactura": $lineasFactura
}"""

facturasRectificadasSustituidas = """{
    "serie": "$serie",
    "numero": $numero,
    "fechaExpedicion": "$fechaExpedicion"
}"""

factura_correcion = """{
    "produccion": $produccion,
    "descripcion": "$descripcion",
    "fechaOperacion": "$fechaOperacion",
    "fechaExpedicion": "$fechaExpedicion",
    "serie": "$serie",
    "numeroFactura": $numeroFactura,
    "simplificada": $simplificada,
    "facturaEmitidaSustitucionSimplificada": $facturaEmitidaSustitucionSimplificada,
    "codigoFacturaRectificativa": "$codigoFacturaRectificativa",
    "tipoFacturaRectificativa": "$tipoFacturaRectificativa",
    "baseRectificativa": $baseRectificativa,
    "cuotaRectificada": $cuotaRectificada,
    "cuotaRecargoRectificada": $cuotaRecargoRectificada,
    "emisor": $emisor,
    "destinatario": $destinatario,  
    "lineasFactura": $lineasFactura,
    "facturasRectificadasSustituidas": $facturasRectificadasSustituidas
}"""

customer = """{
    "nif": "$nif",
    "nombreoRazonSocial": "$nombreoRazonSocial",
    "apellido1": "$apellido1",
    "apellido2": "$apellido2",
    "municipio": "$municipio",
    "codigoPostal": "$codigoPostal",
    "direccion": "$direccion",
    "email": "$email",
    "tipoLicencia": "$tipoLicencia",
    "tipoCertificado": "$tipoCertificado",
    "clavesIVA": $clavesIVA
}"""

temisor_factura = MiTemplate(emisor_factura)
tdestinatario_factura_extranjero = MiTemplate(destinatario_factura_extranjero)
tdestinatario_factura = MiTemplate(destinatario_factura)
tlinea_factura = MiTemplate(linea_factura)
tfactura = MiTemplate(factura)
tfacturasRectificadasSustituidas = MiTemplate(facturasRectificadasSustituidas)
tfactura_correcion = MiTemplate(factura_correcion)
tcustomer = MiTemplate(customer)
