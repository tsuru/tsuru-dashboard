var db = new EmbeddedDashboard();

// get kpi group data and set update
var kpiGroup = new KPIGroupComponent();
kpiGroup.setDimensions(12, 2);
$.ajax({
    url: "/dashboard/cloud_status",
    success: function(data) {
        kpiGroup.addKPI('total_apps', {
            caption: 'Apps',
            value: data.total_apps,
        });
        kpiGroup.addKPI('total_containers', {
            caption: 'Units',
            value: data.total_containers,
        });
        kpiGroup.addKPI('total_nodes', {
            caption: 'Nodes',
            value: data.total_nodes,
        });
        kpiGroup.addKPI('containers_by_nodes', {
            caption: 'Units by node',
            value: data.containers_by_nodes,
        });
    }
});
db.addComponent(kpiGroup);

// healing data and set update
var healingKPI = new KPIComponent();
healingKPI.setDimensions(6, 3);
healingKPI.setCaption("Healings (last 24h)");
$.ajax({
    url: "/dashboard/healing_status",
    success: function(data) {
        healingKPI.setValue(data.healing);
    }
});
db.addComponent(healingKPI);

// deploy data and set update
var deployGauge = new GaugeComponent();
deployGauge.setDimensions(6, 3);
deployGauge.setCaption("Deploys with error (last 24h)");
deployGauge.lock();

$.ajax({
    url: "/dashboard/deploys",
    success: function(data) {
        deployGauge.setLimits(0, data.last_deploys);
        deployGauge.setValue(data.errored, {});
        deployGauge.unlock();
    }
});
db.addComponent(deployGauge);

db.embedTo("application");
