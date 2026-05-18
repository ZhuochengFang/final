CLS_swing = [0,98, 118, 138, 157, 177, 196, 216, 235, 254, 273, 291, 309, 327, 344, 361,];
CLS_gain = [175, 174, 173, 171, 169, 166, 163, 158, 151, 140, 122, 104, 88, 76, 66, 58];

CLS_swing_double = CLS_swing/2;
CLS_gain_dB = 20*log10(CLS_gain);

len= length(CLS_swing_double);

% --- Plot with interpolation for a smooth curve ---
x = CLS_swing_double; % horizontal axis
y = CLS_gain_dB;      % vertical axis (dB)

% Create a finer grid and interpolate using shape-preserving piecewise cubic (pchip)
xq = linspace(min(x), max(x), 500);
yq = interp1(x, y, xq, 'pchip');

figure('Color','w'); hold on; box on;
plot(xq, yq, '-','LineWidth',2, 'Color',[0 0.4470 0.7410]); % smooth curve
scatter(x, y, 48, [0.8500 0.3250 0.0980], 'filled'); % original points

xlabel('CLS_{swing}/2');
ylabel('Gain (dB)');
title('Linearity: CLS swing vs gain (dB)');
grid on;
set(gca,'FontSize',12);

% Ensure output directory exists and save the figure
outdir = fullfile('doc_thesis','figs','04');
if ~exist(outdir, 'dir')
	mkdir(outdir);
end
outfile = fullfile(outdir, 'linearity.png');
print(gcf, outfile, '-dpng', '-r300');
fprintf('Saved plot to: %s\n', outfile);

hold off;
