(function(){

var ZC = Ext.ns('Zenoss.component');


function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.FSP3000R7RamanUPortPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'FSP3000R7RamanUPort',
            fields: [
                {name: 'uid'},
                {name: 'severity'},
                {name: 'name'},
                {name: 'interfaceConfigId'},
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
                id: 'interfaceConfigId',
                dataIndex: 'interfaceConfigId',
                header: _t('Comment'),
                sortable: true,
                width: 400
            },{
                id: 'inventoryUnitName',
                dataIndex: 'inventoryUnitName',
                header: _t('Model'),
                sortable: true,
                width: 300
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
        ZC.FSP3000R7RamanUPortPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('FSP3000R7RamanUPortPanel', ZC.FSP3000R7RamanUPortPanel);
ZC.registerName('FSP3000R7RamanUPort', _t('Raman Upgrade Port'),_t('Raman Upgrade Ports'));
})();


