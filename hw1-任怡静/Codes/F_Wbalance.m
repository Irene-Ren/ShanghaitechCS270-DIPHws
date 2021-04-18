function ret = F_Wbalance(input)
    R = input(:,:,1);
    G = input(:,:,2);
    B = input(:,:,3);

    [M,N,~] = size(input);
    input = im2double(input);

    % method 1
    I_gray = 0.299 .* R + 0.587 .* G + 0.114 .* B;
    I_bar = mean(I_gray,'all');
    R_bar = mean(R,'all');
    G_bar = mean(G,'all');
    B_bar = mean(B,'all');
    k_matrix = zeros(3,3);
    k_matrix(1,1) = I_bar/R_bar;
    k_matrix(2,2) = I_bar/G_bar;
    k_matrix(3,3) = I_bar/B_bar;
    ret = zeros(M,N,3);
    for i = 1:M-1
        for j = 1:N-1
            ret(i,j,:) = k_matrix * squeeze(input(i,j,:));
        end
    end

    ret = im2uint8(ret);
end