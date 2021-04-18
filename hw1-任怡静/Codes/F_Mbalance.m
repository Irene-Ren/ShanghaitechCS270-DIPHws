function ret = F_Mbalance(input)
    R = input(:,:,1);
    G = input(:,:,2);
    B = input(:,:,3);

    [M,N,~] = size(input);
    input = im2double(input);

    S_rgb = min([max(R(:)),max(G(:)), max(B(:))]);
    N_max = max([sum(R(:)>S_rgb),sum(G(:)>S_rgb),sum(B(:)>S_rgb)]);
    sorted_R = sort(R(:));
    T_r = sorted_R(end - N_max);
    sorted_G = sort(G(:));
    T_g = sorted_G(end - N_max);
    sorted_B = sort(B(:));
    T_b = sorted_B(end - N_max);
    k_matrix = zeros(3,3);
    k_matrix(1,1) = S_rgb/T_r;
    k_matrix(2,2) = S_rgb/T_g;
    k_matrix(3,3) = S_rgb/T_b;

    T = zeros(M,N,3);
    for i = 1:M-1
        for j = 1:N-1
            T(i,j,:) = k_matrix * squeeze(input(i,j,:));
        end
    end
    ret = im2uint8(T);
end