function gotEmployees(data) {
    console.log(data);
    $("span.info")[0].innerHTML = "Loaded";
    $("#userdetails")[0].innerHTML=`<h1> Details for ${data.fname}  ${data.lname}</h1>
    <h2> ${data.title} </h2>
    <table>
      <tr>
        <th> First name </th>
        <td> ${data.fname}</td>
      </tr>
      <tr>
        <th> Last name </th>
        <td> ${data.lname}</td>
      </tr>
      <tr>
        <th> Email </th>
        <td> ${data.email}</td>
      </tr>

      <tr>
        <th> Phone </th>
        <td> ${data.phone}</td>
      </tr>
    </table>
`



}

$(function() {
    $("a.userlink").click(function (ev) {
        $("span.info")[0].innerHTML = "Loading...";
        $.get(ev.target.href, gotEmployees);
        ev.preventDefault();
        });
});
