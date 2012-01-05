(function(){

var ZC = Ext.ns('Zenoss.component');


function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.FSP3000R7PowerSupplyPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'FSP3000R7PowerSupply',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'name'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'status'},
                {name: 'inventoryUnitName'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 50
            },{
                id: 'name',
                dataIndex: 'name',
                header: _t('Name'),
                sortable: true,
                width: 200
            },{
                id: 'inventoryUnitName',
                dataIndex: 'inventoryUnitName',
                header: _t('Model'),
                sortable: true,
                width: 400
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                sortable: true
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Status'),
                renderer: Zenoss.render.pingStatus,
            }]
        });
        ZC.FSP3000R7PowerSupplyPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('FSP3000R7PowerSupplyPanel', ZC.FSP3000R7PowerSupplyPanel);
ZC.registerName('FSP3000R7PowerSupply', _t('Power Supply'), _t('Power Supplies'));
})();


