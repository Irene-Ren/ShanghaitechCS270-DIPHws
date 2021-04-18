function ret = F_ColorCorrection(input, reference)
%     lms2lab_1 = [1/sqrt(3) 0 0;
%                  0 1/sqrt(6) 0;
%                  0 0 1/sqrt(2)];
%     lms2lab_2 = [1 1 1;
%                  1 1 -2;
%                  1 -1 0];
%     lms2rgb = [4.4679 -3.5873 0.1193;
%                -1.2186 2.3809 -0.1624;
%                0.0497 -0.2439 1.2045];
    [row,col,~] = size(input);
    L = input(:,:,1);
    A = input(:,:,2);
    B = input(:,:,3);
    correction = zeros(row,col,3);
%     lms = zeros(row,col,3);
%     rgb = zeros(row,col,3);
    
    L_bar = mean(L,'all');
    A_bar = mean(A,'all');
    B_bar = mean(B,'all');
    L_sdev = std(L,1,'all');
    A_sdev = std(A,1,'all');
    B_sdev = std(B,1,'all');
    
    L_tbar = mean(reference(:,:,1),'all');
    A_tbar = mean(reference(:,:,2),'all');
    B_tbar = mean(reference(:,:,3),'all');
    L_tdev = std(reference(:,:,1),1,'all');
    A_tdev = std(reference(:,:,2),1,'all');
    B_tdev = std(reference(:,:,3),1,'all');
    
%     correction(:,:,1) = (L_tdev/L_sdev) .* (L - L_bar) + L_tbar
%     correction(:,:,2) = (A_tdev/A_sdev) .* (A - A_bar) + A_tbar
%     correction(:,:,3) = (B_tdev/B_sdev) .* (B - B_bar) + B_tbar
    
    for i= 1:row
        for j = 1:col
            correction(i,j,1) = (L_tdev/L_sdev) .* (L(i,j) - L_bar) + L_tbar;
            correction(i,j,2) = (A_tdev/A_sdev) .* (A(i,j) - A_bar) + A_tbar;
            correction(i,j,3) = (B_tdev/B_sdev) .* (B(i,j) - B_bar) + B_tbar;
%             lms(i,j,:) = lms2lab_2 * lms2lab_1 * squeeze(correction(i,j,:));
%             for s = 1:3
%                 lms(i,j,s) = 10^lms(i,j,s);
%             end
%             rgb(i,j,:) = lms2rgb * squeeze(lms(i,j,:));
        end
    end
    ret = correction;
    
end