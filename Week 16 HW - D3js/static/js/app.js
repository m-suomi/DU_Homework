//LEVEL 1: D3 DABBLER//
// You need to create a scatter plot between two of the data variables such as Healthcare vs. Poverty or 
// Smokers vs. Age.

// Using the D3 techniques we taught you in class, create a scatter plot that represents each state with
// circle elements. You'll code this graphic in the app.js file of your homework directory—make sure you 
// pull in the data from data.csv by using the d3.csv function. Your scatter plot should ultimately appear
// like the image at the top of this section.

// -Include state abbreviations in the circles.
// -Create and situate your axes and labels to the left and bottom of the chart.
// -Note: You'll need to use python -m http.server to run the visualization. This will host the page at localhost:8000 in your web browser.


// LEVEL 2: Impress the Boss (Optional Challenge Assignment)

// Why make a static graphic when D3 lets you interact with your data?
// 1. More Data, More Dynamics
// You're going to include more demographics and more risk factors. Place additional labels in your scatter plot and give them click events
// so that your users can decide which data to display. Animate the transitions for your circles' locations as well as the range of your axes.
// Do this for two risk factors for each axis. Or, for an extreme challenge, create three for each axis.
// Hint: Try binding all of the .csv data to your circles. This will let you easily determine their x or y values when you click the labels.

// 2. Incorporate d3-tip
// While the ticks on the axes allow us to infer approximate values for each circle, it's impossible to determine the true value without adding
// another layer of data. Enter tooltips: developers can implement these in their D3 graphics to reveal a specific element's data when the user
// hovers their cursor over the element. Add tooltips to your circles and display each tooltip with the data that the user has selected. Use the
// d3-tip.js plugin developed by Justin Palmer—we've already included this plugin in your assignment directory.


// Create SVG size/margin variables for layout
var svgWidth = 960;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper
var svg = d3
  .select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Append an SVG group for the chart and shift by left and top margins
var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Get data from csv file
// d3.csv("static/data/data.csv", function(err, data) {
//     if (err) throw err;

d3.csv("static/data/data.csv").then(data => {
    console.log(data);
    
    //parse data to integer types
    data.forEach(stateData => {
        stateData.id = +stateData.id;
        stateData.poverty = +stateData.poverty;
        stateData.povertyMoe = +stateData.povertyMoe;
        stateData.age = +stateData.age;
        stateData.ageMoe = +stateData.ageMoe;
        stateData.income = +stateData.income;
        stateData.incomeMoe = +stateData.incomeMoe;
        stateData.healthcare = +stateData.healthcare
        stateData.healthcareLow = +stateData.healthcareLow;
        stateData.healthcareHigh = +stateData.healthcareHigh;
        stateData.obesity = +stateData.obesity;
        stateData.obesityLow = +stateData.obesityLow;
        stateData.obesityHigh = +stateData.obesityHigh;
        stateData.smokes = +stateData.smokes;
        stateData.smokesLow = +stateData.smokesLow;
        stateData.smokesHigh = +stateData.smokesHigh;
    });
    

    //define scales
    console.log(d3.extent(data, d=> d.poverty))
    xScaleMin = d3.min(data, d=> d.poverty)
    xScaleMax = d3.max(data, d=> d.poverty)
    xScaleLen = xScaleMax - xScaleMin
    console.log(xScaleMin, xScaleMax, xScaleLen)
    var xScale = d3.scaleLinear()
                    .domain([xScaleMin - .05*xScaleLen, xScaleMax + .05*xScaleLen]) //go a little above and below the min/max so poitns aren't directly on axis
                    .range([0, width]);
    
    console.log(d3.extent(data, d=> d.healthcare))
    yScaleMin = d3.min(data, d=> d.healthcare)
    yScaleMax = d3.max(data, d=> d.healthcare)
    yScaleLen = yScaleMax - yScaleMin
    console.log(yScaleMin, yScaleMax, yScaleLen)
    var yScale = d3.scaleLinear()
                    .domain([yScaleMin - .05*yScaleLen, yScaleMax + .05*yScaleLen]) //go a little above and below the min/max so poitns aren't directly on axis
                    .range([height, 0]);
    

    //create and append axes to chartGroup
    var xAxis = chartGroup.append("g")
                .attr("transform", `translate(0, ${height})`)
                .call(d3.axisBottom(xScale));
    
    var yAxis = chartGroup.append("g")
                .call(d3.axisLeft(yScale));
    
    //create axes labels
    var xAxisLabel = chartGroup.append("text")
                        .attr("transform", `translate(${width / 2}, ${height + margin.top + 20})`)
                        .attr("text-anchor", "middle")
                        .attr("font-size", "14px")
                        .attr("fill", "black")
                        .attr("font-weight", "bold")
                        .text("State Population in Poverty (%)");

    var yAxisLabel = chartGroup.append("text")
                        .attr("transform", `translate(-30, ${height/2})rotate(-90)`)
                        .attr("text-anchor", "middle")
                        .attr("font-size", "14px")
                        .attr("fill", "black")
                        .attr("font-weight", "bold")
                        .text("State Population Lacking Healthcare (%)");


    //initialize tooltip so that can hover over data to see more details
    var toolTip = d3.tip()
                    .attr("class", "d3-tip")
                    .offset([80, -60])
                    .html((d,i) => {
                        return (`<strong>${d.state}</strong>
                        <br>Poverty: ${d.poverty}%
                        <br>Lack Healthcare: ${d.healthcare}%`)});
    //add tooltip to chartGroup
    chartGroup.call(toolTip);


    //apend circles and text to data in chartGroup
    let circleRadius = 12;
    let textPixels = circleRadius - 1;
    
    var circlesGroup = chartGroup.selectAll(".stateCircle")
                        .data(data)
                        .enter()
                        .append("circle")
                        .attr("class", "stateCircle")
                        .attr("cx", (d, i) => xScale(d.poverty))
                        .attr("cy", (d, i) => yScale(d.healthcare))
                        // .attr("fill", d3.rgb(136, 178, 247)) //already defined in d3Style.css
                        .attr("r", circleRadius)
                        //create mousover event listener to display tooltip when over a certain state and mouseout to hide it when move off the state
                        .on("mouseover", toolTip.show)    
                        .on("mouseout", toolTip.hide);
    
                        
    var stateAbbrGroup = chartGroup.selectAll(".stateText")
                        .data(data)
                        .enter()
                        .append("text")
                        .attr("class", "stateText")
                        .attr("dx", (d, i) => xScale(d.poverty))
                        .attr("dy", (d, i) => yScale(d.healthcare)+textPixels/3)
                        .attr("font-size", `${textPixels}px`)
                        // .attr("text-anchor", "middle") //already defined is d3Style.css
                        // .attr("fill", "white") //already defined is d3Style.css
                        .text((d, i) => d.abbr);


});