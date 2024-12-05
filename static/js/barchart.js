// Test data
const color = d3.scaleOrdinal(d3.schemeCategory10);  // Color scale for the bars

// Margin and dimensions for the SVG container
const margin = { top: 10, right: 20, bottom: 40, left: 40 };
const width = 500 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

// Function to render the bar chart
function render(data, selector, categories) {
    // Select the SVG container and set its dimensions
    const svg = d3.select(selector)
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    // Append a group element to the SVG and apply a transformation
    const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    // Create the x-scale using a band scale
    const x = d3.scaleBand()
        .domain(data.map((d, i) => i))  // Map data indices to the x-scale
        .rangeRound([0, width])
        .padding(0.1);

    // Determine the maximum value in the data
    const maxValue = d3.max(data);
    // Create the y-scale using a linear scale
    const y = d3.scaleLinear()
        .domain(maxValue === 0 ? [0, 1] : [0, maxValue])  // Handle all-zero data
        .range([height, 0]);

    // Create the y-axis with custom tick formatting
    const yAxis = d3.axisLeft(y)
        .ticks(5)
        .tickFormat(d => (maxValue === 0 ? "0" : d));  // Show only "0" if all data values are zero

    // Append the x-axis to the group element
    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x).tickFormat(i => categories[i]))  // Format ticks with category names
        .selectAll(".tick text")
        .attr("class", "axis-label");

    // Append the y-axis to the group element
    g.append("g")
        .attr("class", "axis axis--y")
        .call(yAxis)
        .append("text")
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("y", -margin.left + 10)
        .attr("x", -height / 2)
        .attr("dy", "0.71em")
        .attr("text-anchor", "middle");

    // Create a tooltip div element
    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);  // Initially hidden

    // Append rectangles for the bar chart
    g.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", (d, i) => x(i))  // Set x position based on the x-scale
        .attr("y", d => y(d))  // Set y position based on the y-scale
        .attr("width", x.bandwidth())  // Set the width of the bars
        .attr("height", d => height - y(d))  // Set the height of the bars
        .attr("fill", (d, i) => color(i))  // Set the fill color based on the color scale
        .on("mouseover", function (event, d) {
            tooltip.transition().duration(200).style("opacity", 0.9);  // Show tooltip
            tooltip.html("Count: "+ d)  // Set content
                .style("left", (event.pageX + 0) + "px")  // Position to the right of mouse
                .style("top", (event.pageY - 28) + "px");  // Position above mouse
        })
        .on("mouseout", function () {
            tooltip.transition().duration(200).style("opacity", 0);  // Hide tooltip
        });
}


let input = [0, 0, 0, 0, 0, 0];
let input2 = [0, 0];
let input3 = [0, 0, 0, 0, 0, 0];
let input4 = [0, 0];

const categories_2 = ["URL", "Non-URL"]; // Categories for version methods
const categories = ["SemVer_3", "SemVer_2", "V*", "Integer", "Date", "Others"];  // Categories for the version formats

// Function to update the barchart with new data
function update_render(api_v_formats, api_v_methods, endpoint_v_formats, endpoint_v_methods) {
    d3.select("#barchart").selectAll("*").remove();  // Clear the existing chart
    d3.select("#barchart2").selectAll("*").remove();  // Clear the existing chart
    d3.select("#barchart3").selectAll("*").remove();  // Clear the existing chart
    d3.select("#barchart4").selectAll("*").remove();  // Clear the existing chart
    render(api_v_formats, "#barchart", categories);  // Render the chart with new data
    render(api_v_methods, "#barchart2", categories_2);
    render(endpoint_v_formats, "#barchart3", categories);
    render(endpoint_v_methods, "#barchart4", categories_2);
}

// Initial render of the API barcharts
render(input, "#barchart", categories);
render(input2, "#barchart2", categories_2);

// Initial render of the Endpoint barcharts
render(input3, "#barchart3", categories);
render(input4, "#barchart4", categories_2);

