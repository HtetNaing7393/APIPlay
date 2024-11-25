
// Test data
// let input = [0, 0, 0, 0, 0, 0];
// const categories = ["SemVer_3", "SemVer_2", "V*", "Integer", "Date", "Others"]
// const color = d3.scaleOrdinal(d3.schemeCategory10);


// const margin = { top: 10, right: 20, bottom: 40, left: 40 };
// const width = 500 - margin.left - margin.right;
// const height = 400 - margin.top - margin.bottom;

// function render(data, selector) {
//     const svg = d3.select(selector),
//         g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

//     const x = d3.scaleBand()
//         .domain(data.map((d, i) => i))
//         .rangeRound([0, width])
//         .padding(0.1);

//     const y = d3.scaleLinear()
//         .domain([0, d3.max(data)])
//         .nice()
//         .range([height, 0]);

//     const yAxis = d3.axisLeft(y)
//         .tickValues(data)  // Set the tick values to the actual data values
//         .tickFormat(d3.format("d"));  // Format the ticks as integers

//     g.append("g")
//         .attr("class", "axis axis--x")
//         .attr("transform", `translate(0,${height})`)
//         .call(d3.axisBottom(x).tickFormat(i => categories[i]))
//         .selectAll(".tick text")
//         .attr("class", "axis-label");

//     g.append("g")
//         .attr("class", "axis axis--y")
//         .call(yAxis)
//         .append("text")
//         .attr("class", "axis-label")
//         .attr("transform", "rotate(-90)")
//         .attr("y", 6)
//         .attr("dy", "0.71em")
//         .attr("text-anchor", "end")
//         .text("Value");

//     g.selectAll(".bar")
//         .data(data)
//         .enter().append("rect")
//         .attr("class", "bar")
//         .attr("x", (d, i) => x(i))
//         .attr("y", d => y(d))
//         .attr("width", x.bandwidth())
//         .attr("height", d => height - y(d))
//         .attr("fill", (d, i) => color(i));

// }


// function update_render(new_input) {
//     d3.select("#barchart").selectAll("*").remove();
//     render(new_input, "#barchart");
// }

// render(input, "#barchart");


// Test button for selenium

