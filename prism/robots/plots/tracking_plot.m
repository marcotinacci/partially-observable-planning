%=========================================
%Generated by PRISM Chart Package
%=========================================

x0 = [1.0 5.0 9.0 13.0 17.0 ];
y0 = [0.0 0.4 0.48000000000000004 0.556416 0.61462528 ];
x1 = [0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 11.0 12.0 13.0 14.0 15.0 16.0 17.0 18.0 19.0 20.0 ];
y1 = [0.0 0.0 0.0 0.4 0.4 0.4 0.4 0.48000000000000004 0.48000000000000004 0.48000000000000004 0.48000000000000004 0.5299200000000001 0.556416 0.556416 0.556416 0.5865728 0.61462528 0.61462528 0.61462528 0.63739904 0.66470912 ];

figure1 = figure('Color', [1 1 1], 'PaperPosition',[0.6345 6.345 20.3 15.23],'PaperSize',[20.98 29.68]);

axes1 = axes('Parent', figure1, 'FontSize', 16);
xlabel(axes1, 'k');
ylabel(axes1, 'Minimum probability');
box(axes1, 'on');
hold(axes1, 'all');

title(axes1,[])
plot0 = plot(x0, y0, 'o-', 'Parent', axes1, 'LineWidth', 2);
plot1 = plot(x1, y1, 's-', 'Parent', axes1, 'LineWidth', 2);
legend1 = legend(axes1,{'tracking', 'tracking (1)'},'Location', 'EastOutside');
