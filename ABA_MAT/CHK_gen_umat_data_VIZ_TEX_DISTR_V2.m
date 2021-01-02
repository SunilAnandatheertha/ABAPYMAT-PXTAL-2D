function CHK_gen_umat_data_VIZ_TEX_DISTR_V2(grain_orientation_dis, TotalNumGrains, NumGrainsx, NumGrainsy, FNbase, Root_Folder, texinstance)

% grain_orientation_dis
xx = linspace(0, size(grain_orientation_dis,2)+1, size(grain_orientation_dis,2) + 1);
xx = xx - xx(2)/2 + 1;


yy = linspace(0, size(grain_orientation_dis,1)+1, size(grain_orientation_dis,1) + 1);
yy = yy - yy(2)/2 + 1;
[xx, yy] = meshgrid(xx, yy);

Model_origin_x = 0;
Model_origin_y = 0;

Model_Size_x = 100;
Model_Size_y = 006;

xx = Model_Size_x*xx/max(max(xx));
yy = Model_Size_y*yy/max(max(yy));

patches = cell(size(grain_orientation_dis));
for r = 1:size(grain_orientation_dis, 1)
    for c = 1:size(grain_orientation_dis, 2)
        patches{r,c} = [xx(r, c)     yy(r,c);
                        xx(r+1, c)   yy(r+1,c);
                        xx(r+1, c+1) yy(r+1,c+1);
                        xx(r, c+1)   yy(r,c+1)];
    end
end
figurehandle = figure;
hold on
patchcolors = {'g', 'b', 'r', 'm', 'c'};
if TotalNumGrains > 200
    PatchEdgeColorValue = 'none';
else
    PatchEdgeColorValue = 'k';
end

for count = 1:numel(patches)
    patch(patches{count}(:,1)', patches{count}(:,2)', patchcolors{grain_orientation_dis(count)}, 'EdgeColor', PatchEdgeColorValue)
end

axis([Model_origin_x Model_Size_x Model_origin_y Model_Size_y])
axis tight
axis equal
TitleTextLine1 = [num2str(TotalNumGrains) '_' num2str(NumGrainsx) '_' num2str(NumGrainsy) '_' FNbase];

ht = title(TitleTextLine1);
axis tight
set(gca, 'fontsize', 14)
set(ht,  'fontsize', 8)
set(ht, 'FontWeight', 'normal')
set(gca,'XColor', 'none','YColor','none')

imagename = [FNbase '.tiff'];
imagefilepath = [Root_Folder 'TEX_DISTRIBUTION_INFO\'];
imagefilepathname = [imagefilepath imagename];
axis equal
axis tight
pause(0.1)
print('-dtiff', imagefilepathname)
pause(0.1)
if texinstance == 1
    figure
    cbh = colorbar('Ticks',[1, 2, 3, 4, 5, 6], 'TickLabels', {'W','G','B','C','S', '.'}, 'location', 'southoutside');
    haha = colormap([0 1 0;
                     0 0 1;
                     1 0 0;
                     1 0 1;
                     0 1 1]);
    cpos = cbh.Position;

    set(cbh, 'Position', [1.5*cpos(1) 1.8*cpos(2) 0.8*cpos(3) 3*cpos(4)])
    set(cbh, 'fontsize', 12)
    set(gca, 'visible', 'off')
    set(cbh, 'FontWeight', 'normal')
    set(cbh, 'FontWeight', 'normal')
    caxis([1 5])
    set(cbh, 'TickLength',0)
    cbarimagename = 'TEX_cbar';
    cbarimagefilepathname = [imagefilepath cbarimagename];
    print('-dtiff', cbarimagefilepathname)
end
pause(0.1)
end