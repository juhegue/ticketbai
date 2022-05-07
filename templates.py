# -*- coding: utf-8 -*-

from string import Template

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
    "lineasFactura": [$lineasFactura]
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
    "emisor": $emisor_factura,
    "destinatario": $destinatario_factura,  
    "lineasFactura": [$lineas_factura]
    "facturaEmitidaSustitucionSimplificada": $facturaEmitidaSustitucionSimplificada,
    "codigoFacturaRectificativa": "$codigoFacturaRectificativa",
    "tipoFacturaRectificativa": "$tipoFacturaRectificativa",
    "baseRectificativa": $baseRectificativa,
    "cuotaRectificada": $cuotaRectificada,
    "cuotaRecargoRectificada": $cuotaRecargoRectificada,
    "facturasRectificadasSustituidas": [$facturasRectificadasSustituidas]
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
    "clavesIVA": [$clavesIVA],
    "tipoCertificado": "$tipoCertificado"
}"""

temisor_factura = Template(emisor_factura)
tdestinatario_factura_extranjero = Template(destinatario_factura_extranjero)
tdestinatario_factura = Template(destinatario_factura)
tlinea_factura = Template(linea_factura)
tfactura = Template(factura)
tfacturasRectificadasSustituidas = Template(facturasRectificadasSustituidas)
tfactura_correcion = Template(factura_correcion)
tcustomer = Template(customer)
