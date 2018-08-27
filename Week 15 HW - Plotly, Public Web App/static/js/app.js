//populates side panel with all of the sample's metadata
function buildMetadata(sample) {
  //use flask api route for metadata that returns a json
  let metadataURL = `/metadata/${sample}`
  // Use `d3.json` to fetch the metadata for a sample
  d3.json(metadataURL).then(function(sampleMetadata) {
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
  var degrees = 170 - (WFREQ * 18), //convert WREQ to degrees make 10 ranges for each number 0-9 and want to place marker at mid-pt of each range
      radius = .5;
  var radians = degrees * Math.PI / 180;
  var x = radius * Math.cos(radians);
  var y = radius * Math.sin(radians);

  // Path of the triangular gauge meter
  var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
      pathX = String(x),
      space = ' ',
      pathY = String(y),
      pathEnd = ' Z';
  var path = mainPath.concat(pathX,space,pathY,pathEnd);

  var data = [{ type: 'scatter',
      x: [0], y:[0],
      marker: {size: 28, color:'850000'},
      showlegend: false,
      name: 'Wash Frequency',
      text: WFREQ,
      hoverinfo: 'text+name'},

    { values: [50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50/10, 50],
    rotation: 72, //seems like a bug that we have to rotate by 72 degrees, instead of 90 to appear correctly
    direction: "counterclockwise",
    sort: false, //including this prevented a weird chrome mis-rendering that re-arranged the order incorrectly
    text: ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', ''],
    textinfo: 'text',
    textposition:'inside',
    marker: {colors:['rgba(0, 115, 0, .5)',  
                      'rgba(14, 127, 12.5, .5)','rgba(41,139,25, .5)',
                      'rgba(69,152,51, .5)', 'rgba(96,164,76, .5)', 
                      'rgba(123,177,101, .5)', 'rgba(150,189,126, .5)',
                      'rgba(178,201,152, .5)', 'rgba(205,214,177, .5)',
                      'rgba(232,226,202, .5)', 'rgba(255, 255, 255, 0)']},
    labels: ['9', '8', '7', '6', '5', '4', '3', '2', '1', '0', ' '],
    hoverinfo: 'label',
    hole: .5,
    type: 'pie',
    showlegend: false
  }];

  var layout = {
    shapes:[{
        type: 'path',
        path: path,
        fillcolor: '850000',
        line: {
          color: '850000'
        }
      }],
    title: "Belly Button Washing Frequency <br> Scrubs per Week",
    // height: 1000,
    // width: 1000,
    xaxis: {zeroline:false, showticklabels:false,
              showgrid: false, range: [-1, 1]},
    yaxis: {zeroline:false, showticklabels:false,
              showgrid: false, range: [-1, 1]}
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
      values: sampleData.sample_values.slice(0,10),
      labels: sampleData.otu_ids.slice(0,10),
      hovertext: sampleData.otu_labels.slice(0,10),
      type: 'pie'
    }];

    let layout = {
      title: 'Top Ten Microbial Species (OTUs)<br> by Amount in Sample',
    };
    
    Plotly.newPlot("pie", data, layout);

    // Build a Bubble Chart using the sample data
    let dataB = [{
      x: sampleData.otu_ids,
      y: sampleData.sample_values,
      text: sampleData.otu_labels,
      mode: 'markers',
      marker: {
        size: sampleData.sample_values,
        color: sampleData.otu_ids
        }
    }];
    
    let layoutB = {
      title: 'Amount of All Microbial Species (OTUs) Present in Sample',
      xaxis: {title: 'OTU IDs'},
      yaxis: {title: 'Amount in Sample'},
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
