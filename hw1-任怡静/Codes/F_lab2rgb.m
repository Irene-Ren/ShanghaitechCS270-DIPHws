function ret = F_lab2rgb(input)
    [row,col,~] = size(input);
    lms = zeros(row,col,3);
    rgb = zeros(row,col,3);
    lms2lab_1 = [1/sqrt(3) 0 0;
                 0 1/sqrt(6) 0;
                 0 0 1/sqrt(2)];
    lms2lab_2 = [1 1 1;
                 1 1 -2;
                 1 -1 0];
    lms2rgb = [4.4679 -3.5873 0.1193;
               -1.2186 2.3809 -0.1624;
               0.0497 -0.2439 1.2045];
    for i = 1:row
        for j = 1:col
            lms(i,j,:) = lms2lab_2 * lms2lab_1 * squeeze(input(i,j,:));
            for s = 1:3
                lms(i,j,s) = 10^lms(i,j,s);
            end
            rgb(i,j,:) = lms2rgb * squeeze(lms(i,j,:));
        end
    end
    ret = rgb;
end