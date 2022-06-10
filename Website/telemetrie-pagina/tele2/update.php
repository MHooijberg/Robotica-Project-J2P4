<script type="text/JavaScript">

function updateText(objectId, text) {
    document.getElementById(objectId).textContent = text;
}
function updateHTML(objectId, html) {
    document.getElementById(objectId).innerHTML = html;
}
function updateDisplay() {

<?php
    echo "\n\t\t\t\tupdateText(\"host\",\"$host\");";
    echo "\n\t\t\t\tupdateText(\"model\",\"$model\");";
    echo "\n\t\t\t\tupdateHTML(\"time\",\"$current_time\");";
    echo "\n\t\t\t\tupdateText(\"kernel\",\"$system\" + \" \" + \"$kernel\");";
    echo "\n\t\t\t\tupdateText(\"processor\",\"$processor\");";
    echo "\n\t\t\t\tupdateText(\"freq\",\"$frequency\" + \"MHz\");";
    echo "\n\t\t\t\tupdateText(\"loadavg\",\"$loadaverages\");";
    echo "\n\t\t\t\tupdateHTML(\"cpu_temperature\",\"$cpu_temperature\" + \"&#x2103;\");";
    echo "\n\t\t\t\tupdateText(\"uptime\",\"$uptime\");";

    echo "\n\t\t\t\tupdateText(\"total_mem\",\"$total_mem\" );";
    echo "\n\t\t\t\tupdateText(\"used_mem\",\"$used_mem\" );";
    echo "\n\t\t\t\tupdateText(\"percent_used\",\"$percent_used%\");";
    echo "\n\t\t\t\tupdateText(\"free_mem\",\"$free_mem\" );";
    echo "\n\t\t\t\tupdateText(\"percent_free\",\"$percent_free%\");";
    echo "\n\t\t\t\tupdateText(\"buffer_mem\",\"$buffer_mem\" );";
    echo "\n\t\t\t\tupdateText(\"percent_buff\",\"$percent_buff%\");";
    echo "\n\t\t\t\tupdateText(\"cache_mem\",\"$cache_mem\" );";
    echo "\n\t\t\t\tupdateText(\"percent_cach\",\"$percent_cach%\");";

    echo "\n\t\t\t\tupdateText(\"total_swap\",\"$total_swap\" );";
    echo "\n\t\t\t\tupdateText(\"used_swap\",\"$used_swap\" );";
    echo "\n\t\t\t\tupdateText(\"percent_swap\",\"$percent_swap%\");";
    echo "\n\t\t\t\tupdateText(\"free_swap\",\"$free_swap\" );";
    echo "\n\t\t\t\tupdateText(\"percent_swap_free\",\"$percent_swap_free%\");\n";
?>

    document.getElementById("bar1").style.width = "<?php echo $percent_used; ?>px";
    document.getElementById("bar2").style.width = "<?php echo $percent_free; ?>px";
    document.getElementById("bar3").style.width = "<?php echo $percent_buff; ?>px";
    document.getElementById("bar4").style.width = "<?php echo $percent_cach; ?>px";
    document.getElementById("bar5").style.width = "<?php echo $percent_swap; ?>px";
    document.getElementById("bar6").style.width = "<?php echo $percent_swap_free; ?>px";
}

</script>