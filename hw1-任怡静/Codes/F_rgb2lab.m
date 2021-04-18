function ret = F_rgb2lab(input)
    input = im2double(input);
    [row,col,~] = size(input);
    rgb2lms = [0.3811 0.5783 0.0402;
               0.1967 0.7244 0.0782;
               0.0241 0.1288 0.8444];
    rgb2xyz = [0.5141 0.3239 0.1604;
               0.2651 0.6702 0.0641;
               0.0241 0.1288 0.8444];
    xyz2lms = [0.3897 0.6890 -0.0787;
               -0.2298 1.1834 0.0464;
               0.0000 0.0000 1.0000];
    lms2lab_1 = [1/sqrt(3) 0 0;
                 0 1/sqrt(6) 0;
                 0 0 1/sqrt(2)];
    lms2lab_2 = [1 1 1;
                 1 1 -2;
                 1 -1 0];
    lms = zeros(row,col,3);
    lab = zeros(row,col,3);
    for i= 1:row
        for j = 1:col
            rgb = [input(i,j,1);
                   input(i,j,2);
                   input(i,j,3)];
            temp = xyz2lms * (rgb2xyz * rgb);
            for s = 1:3
                if temp(s) == 0
                    lms(i,j,s) = 0;
                else
                    lms(i,j,s) = log10(temp(s));
                end
            end
            lab(i,j,:) = lms2lab_1 * lms2lab_2 * squeeze(lms(i,j,:));
        end
    end
    ret = lab;
end
