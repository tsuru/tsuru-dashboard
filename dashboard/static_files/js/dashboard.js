var db = new EmbeddedDashboard();

// get kpi group data and set update
var kpiGroup = new KPIGroupComponent();
kpiGroup.setDimensions(12, 2);
kpiGroup.setCaption("Cloud Status");    
kpiGroup.lock();
$.ajax({
    url: "/dashboard/cloud_status",
    success: function(data) {
        kpiGroup.addKPI('total_apps', {
            caption: 'Total de Apps',
            value: data.total_apps,
        });
        kpiGroup.addKPI('total_containers', {
            caption: 'Total de Containers',
            value: data.total_containers,
        });
        kpiGroup.addKPI('total_nodes', {
            caption: 'Total de Nós',
            value: data.total_nodes,
        });
        kpiGroup.addKPI('containers_by_nodes', {
            caption: 'Containers por Nó',
            value: data.containers_by_nodes,
        });
        kpiGroup.unlock();
    },
    error: function(jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown);
        kpiGroup.addKPI('error', {caption: 'error', value: 0});
        kpiGroup.unlock();
    }
});
db.addComponent(kpiGroup);

// healing data and set update
var healingKPI = new KPIComponent();
healingKPI.setDimensions(6, 3);
healingKPI.setCaption("Healing - ultimas 24hrs");    
healingKPI.lock();
$.ajax({
    url: "/dashboard/healing_status",
    success: function(data) {
        healingKPI.setValue(data.length);
        healingKPI.unlock();
    },
    error: function(jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown);
        healingKPI.setValue(0);
        healingKPI.unlock();
    }
});
db.addComponent(healingKPI);

// deploy data and set update
var deployGauge = new GaugeComponent();
deployGauge.setDimensions(6, 3);
deployGauge.setCaption("Deploys com erro - utlimas 24hrs");    
deployGauge.lock();
$.ajax({
    url: "/dashboard/deploys",
    success: function(data) {
        deployGauge.setLimits(0, data.last_deploys.length);
        deployGauge.setValue(data.errored);
        deployGauge.unlock();
    },
    error: function(jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown);
        deployGauge.setValue(0);
        deployGauge.unlock();
    }
});
db.addComponent(deployGauge);

db.embedTo("application");
