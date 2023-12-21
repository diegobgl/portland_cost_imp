from odoo import models, fields, api

class ImportCostingProductLine(models.Model):
    _name = 'import.costing.product.line'
    _description = 'Línea de Producto de Costeo de Importación'

    # Referencia al documento de costeo principal
    costing_id = fields.Many2one('import.costing', string='Documento de Costeo')

    # Detalles del producto
    producto_id = fields.Many2one('product.product', string='Producto')
    codigo_producto = fields.Char(related='producto_id.default_code', string='Código del Producto', readonly=True)
    descripcion_producto = fields.Char(related='producto_id.name', string='Descripción', readonly=True)
    familia_id = fields.Many2one(related='producto_id.categ_id', string='Familia', readonly=True)
    cantidad = fields.Float(string='Cantidad / Kilos o Litros')
    costo_unitario_usd = fields.Float(string='Costo Unitario USD')
    costo_unitario = fields.Float(string='Costo Unitario $')
    tipo_cambio = fields.Float(string='Tipo de Cambio')
    precio_neto_venta_usd = fields.Float(string='Precio Neto Venta USD')
    precio_neto_venta = fields.Float(string='Precio Neto Venta $')
    precio_neto_final_usd = fields.Float(string='Precio Neto Final USD')
    precio_neto_final = fields.Float(string='Precio Neto Final $')

    # Calcula los precios netos y finales en base a las reglas de negocio

    @api.depends('product_lines.costo_unitario_usd')
    def _compute_total_costo_unitario_usd(self):
        for record in self:
            record.total_costo_unitario_usd = sum(line.costo_unitario_usd for line in record.product_lines)

    @api.depends('product_lines.costo_unitario')
    def _compute_total_costo_unitario(self):
        for record in self:
            record.total_costo_unitario = sum(line.costo_unitario for line in record.product_lines)

    @api.depends('expense_lines.monto_gastos_nacionales')
    def _compute_total_monto_gastos_nacionales(self):
        for record in self:
            record.total_monto_gastos_nacionales = sum(expense.monto_gastos_nacionales for expense in record.expense_lines)

class ImportCostingExpenseLine(models.Model):
    _name = 'import.costing.expense.line'
    _description = 'Línea de Gasto de Costeo de Importación'

    # Referencia al documento de costeo principal
    costing_id = fields.Many2one('import.costing', string='Documento de Costeo')

    # Detalles del gasto
    linea = fields.Integer(string='Línea')
    tipo = fields.Char(string='Tipo')
    conceptos = fields.Char(string='Conceptos')
    monto_gastos_nacionales = fields.Float(string='Monto $ Gastos Nacionales')
    monto_usd = fields.Float(string='Monto US$ Dólar')
    tipo_cambio_gastos = fields.Float(string='Tipo Cambio')
    monto = fields.Float(string='Monto $')
    # Realiza los cálculos necesarios para los montos en base a las reglas de negocio

class ImportCosting(models.Model):
    _name = 'import.costing'
    _description = 'Costeo de Importación'

    pedido = fields.Char(string='Pedido')
    margen = fields.Float(string='Margen (%)')
    financiamiento = fields.Char(string='Financiamiento (Cuando Aplique)')
    seguro_credito = fields.Char(string='Seguro Crédito (Cuando Aplique)')
    factor_internacion = fields.Float(string='Factor Internación', default=1.0)

    # Relación con líneas de productos
    product_lines = fields.One2many('import.costing.product.line', 'costing_id', string='Líneas de Producto')

    # Relación con líneas de gastos
    expense_lines = fields.One2many('import.costing.expense.line', 'costing_id', string='Líneas de Gastos')

    # Agrega métodos para calcular totales y subtotales en base a las líneas de productos y gastos

    @api.depends('product_lines.costo_unitario_usd')
    def _compute_total_costo_unitario_usd(self):
        for record in self:
            record.total_costo_unitario_usd = sum(line.costo_unitario_usd for line in record.product_lines)

    @api.depends('product_lines.costo_unitario')
    def _compute_total_costo_unitario(self):
        for record in self:
            record.total_costo_unitario = sum(line.costo_unitario for line in record.product_lines)

    @api.depends('expense_lines.monto_gastos_nacionales')
    def _compute_total_monto_gastos_nacionales(self):
        for record in self:
            record.total_monto_gastos_nacionales = sum(expense.monto_gastos_nacionales for expense in record.expense_lines)


    # Campos computados
    total_costo_unitario_usd = fields.Float(compute='_compute_total_costo_unitario_usd', string='Total Costo Unitario USD')
    total_costo_unitario = fields.Float(compute='_compute_total_costo_unitario', string='Total Costo Unitario $')
    total_monto_gastos_nacionales = fields.Float(compute='_compute_total_monto_gastos_nacionales', string='Total Monto Gastos Nacionales')

    

    
    # Nuevos campos para la vista kanban
    color = fields.Integer(string='Color')
    tag_ids = fields.Many2many('import.costing.tag', string='Etiquetas')
    responsable_id = fields.Many2one('res.users', string='Responsable')
    estado = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
        ('hecho', 'Hecho')
    ], string='Estado', default='borrador')

