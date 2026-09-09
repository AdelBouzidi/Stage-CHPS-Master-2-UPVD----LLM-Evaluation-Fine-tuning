program get_max_triples
    implicit none
    integer, parameter :: n = 5
    integer :: a(n)
    integer :: i, j, k, count
    integer :: result

    ! Initialize array a with a[i] = i*i - i + 1
    do i = 1, n
        a(i) = i*i - i + 1
    end do

    ! Count triples (i, j, k) with i < j < k where sum is divisible by 3
    count = 0
    do i = 1, n-2
        do j = i+1, n-1
            do k = j+1, n
                if (mod(a(i) + a(j) + a(k), 3) == 0) then
                    count = count + 1
                end if
            end do
        end do
    end do

    result = count
    print *, result

end program get_max_triples