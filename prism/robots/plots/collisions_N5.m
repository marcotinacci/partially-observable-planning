%=========================================
%Generated by PRISM Chart Package
%=========================================

x0 = [1.0 5.0 9.0 13.0 17.0 21.0 ];
y0 = [1.0 0.6399999999999999 0.09599999999999986 0.06500351999999976 0.0029009510399997662 3.8757990399651554E-5 ];
x1 = [1.0 5.0 9.0 13.0 17.0 21.0 ];
y1 = [1.0 1.0 0.736 0.6447999999999999 0.1482284646399996 0.03802435092479928 ];
x2 = [1.0 5.0 9.0 13.0 17.0 21.0 ];
y2 = [1.0 1.0 0.9199999999999999 0.8896 0.5055359999999998 0.18856140799999954 ];

figure1 = figure('Color', [1 1 1], 'PaperPosition',[0.6345 6.345 20.3 15.23],'PaperSize',[20.98 29.68]);

axes1 = axes('Parent', figure1, 'FontSize', 16);
xlabel(axes1, 'k');
ylabel(axes1, 'Minimum probability');
box(axes1, 'on');
hold(axes1, 'all');

title(axes1,[])
plot0 = plot(x0, y0, 'o-', 'Parent', axes1, 'LineWidth', 2);
plot1 = plot(x1, y1, 's-', 'Parent', axes1, 'LineWidth', 2);
plot2 = plot(x2, y2, '^-', 'Parent', axes1, 'LineWidth', 2);
legend1 = legend(axes1,{'D=3', 'D=4', 'D=5'},'Location', 'EastOutside');