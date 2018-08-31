//populates side panel with all of the sample's metadata
function buildMetadata(sample) {
  //use flask api route for metadata that returns a json
  let metadataURL = `/metadata/${sample}`
  // Use `d3.json` to fetch the metadata for a sample
  d3.json(metadataURL).then(function (sampleMetadata) {
    console.log(sampleMetadata)

    // Use d3 to select the panel with id of `#sample-metadata`
    let metadataPanel = d3.select('#sample-metadata');
    // Use `.html("") to clear any existing metadata
    metadataPanel.html("");
    //add each metadata key, value pair as a new p tag to panel
    Object.entries(sampleMetadata).forEach(entry => {
      metadataPanel.append('p').text(`${entry[0]}: ${entry[1]}`)
    });

    // BONUS: build the gauge chart with the WREQ data from the metadata json
    buildGauge(sampleMetadata.WFREQ)
  });
}


//BONUS: build a gauge chart with wash frequency (WFREQ) data for values ranging 0-9
function buildGauge(WFREQ) {
  // Trig to calc gauge meter point
  // var degrees = 170 - (WFREQ * 18), //convert WREQ to degrees make 10 ranges for each number 0-9 and want to place marker at mid-pt of each range
  //   radius = .5;
  let degrees = 170 - (WFREQ * 18); //convert WREQ to degrees make 10 ranges for each number 0-9 and want to place marker at mid-pt of each range
  // console.log(degrees)
  let radius = .5;
  // console.log(radius)
  var radians = degrees * Math.PI / 180;
  var x = radius * Math.cos(radians);
  var y = radius * Math.sin(radians);
  // console.log(x, y)

  // Path of the triangular gauge meter
  var mainPath = 'M0 -0.025 L0 0.025 L';
  var pathX = String(x);
  var space = ' ';
  var pathY = String(y);
  var pathEnd = ' Z';
  var path = mainPath.concat(pathX, space, pathY, pathEnd);
  // console.log(path)

  var data = [{
    type: 'scatter',
    x: [0], y: [0],
    marker: { size: 28, color: '850000' },
    showlegend: false,
    name: 'Wash Frequency',
    text: WFREQ,
    hoverinfo: 'text+name'
  },

  {
    values: [50 / 10, 50 / 10, 50 / 10, 50 / 10, 50 / 10, 50 / 10, 50 / 10, 50 / 10, 50 / 10, 50 / 10, 50],
    rotation: 72, //first pie slice starts verticaly and goes to right, so already rotated 18 deg and need to rotate another 72 to get it all flat
    sort: false, //including this prevented a weird chrome mis-rendering that re-arranged the order incorrectly
    text: ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', ''],
    textinfo: 'text',
    textposition: 'inside',
    marker: {
      colors: ['rgba(0, 115, 0, .5)',
        'rgba(14, 127, 12.5, .5)', 'rgba(41,139,25, .5)',
        'rgba(69,152,51, .5)', 'rgba(96,164,76, .5)',
        'rgba(123,177,101, .5)', 'rgba(150,189,126, .5)',
        'rgba(178,201,152, .5)', 'rgba(205,214,177, .5)',
        'rgba(232,226,202, .5)', 'rgba(255, 255, 255, 0)']
    },
    labels: ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', ' '],
    hoverinfo: 'label',
    hole: .5,
    type: 'pie',
    showlegend: false
  }];

  //use jquery to identify the inner width of the bootstrap column where the gauge div is located
  //will use this variable to constrain the height to be equal to this so that aspect ratio stays 1:1
  //and location of gauge marker geometry works correclty no longer how website scaled
  var colWidth = $( "#gauge" ).innerWidth();
  // console.log(colWidth)

  var layout = {
    shapes: [{
      type: 'path',
      path: path,
      fillcolor: '850000',
      line: {
        color: '850000'
      }
    }],
    title: "<b>Belly Button Washing Frequency <br> Scrubs per Week</b>",
    height: colWidth,
    xaxis: {
      zeroline: false, showticklabels: false,
      showgrid: false, range: [-1, 1]
    },
    yaxis: {
      zeroline: false, showticklabels: false,
      showgrid: false, range: [-1, 1]
    }
  };

  Plotly.newPlot('gauge', data, layout);
}


//builds both pie chart and bubble chart using the sample's data
function buildCharts(sample) {
  //use flask api route for samples that returns a json of sampe data
  let sampleURL = `/samples/${sample}`;
  //Use `d3.json` to fetch the sample data for the plots
  d3.json(sampleURL).then(function (sampleData) {
    console.log(sampleData)

    // Build a Pie Chart - only select the top 10 sample values
    // updated the app.py to sort the df desc by sample so it returns a sorted json
    // so can just slice all top ten list items for values, labels, and hoverinfo
    let data = [{
      values: sampleData.sample_values.slice(0, 10),
      labels: sampleData.otu_ids.slice(0, 10).map(id => `OTU ID: ${id}`), //make labels clearer that they are OTU IDs
      hovertext: sampleData.otu_labels.slice(0, 10),
      type: 'pie'
    }];

    let layout = {
      title: '<b>Top Ten Microbial Species (OTUs)<br> by Amount in Sample</b>'
    };

    Plotly.newPlot("pie", data, layout);


    // Build a Bubble Chart using the sample data
    let dataB = [{
      x: sampleData.otu_ids,
      y: sampleData.sample_values,
      //create more customized hover text that labels the ID, Amount, and Category
      text: sampleData.otu_labels.map((label, idx) => { 
        return `Microbial OTU ID: ${sampleData.otu_ids[idx]}<br>Amount in Sample: ${sampleData.sample_values[idx]}<br>Microbial Category: ${label}`
      }),
      hoverinfo: "text",
      mode: 'markers',
      marker: {
        size: sampleData.sample_values,
        color: sampleData.otu_ids
      }
    }];

    let layoutB = {
      title: '<b>Amount of All Microbial Species (OTUs) Present in Sample</b>',
      xaxis: { title: 'OTU IDs' },
      yaxis: { title: 'Amount in Sample' },
      showlegend: false,
    };

    Plotly.newPlot("bubble", dataB, layoutB);
  });
}


//initializes the charts and metadata on first load with the top sample in the dropdown
function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}


//called from the selDataset in index.html, when the selection is changed
//will repopulate charts and metadata with the current sample selection
function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}


// Initialize the dashboard
init();
