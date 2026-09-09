program collatz_odds
    implicit none
    integer :: n
    integer, allocatable :: odd_collatz(:)
    integer :: i, temp

    ! Read input
    read(*,*) n

    ! Generate Collatz sequence and collect odd numbers
    odd_collatz = []
    temp = n
    do while (temp > 0)
        if (mod(temp, 2) == 1) then
            odd_collatz = [odd_collatz, temp]
        end if
        if (temp == 1) exit
        if (mod(temp, 2) == 0) then
            temp = temp / 2
        else
            temp = 3 * temp + 1
        end if
    end do

    ! Sort the odd numbers
    call sort_array(odd_collatz)

    ! Output the result
    print *, odd_collatz

contains

    subroutine sort_array(arr)
        integer, intent(inout) :: arr(:)
        integer :: i, j, temp
        do i = 1, size(arr) - 1
            do j = i + 1, size(arr)
                if (arr(j) < arr(i)) then
                    temp = arr(i)
                    arr(i) = arr(j)
                    arr(j) = temp
                end if
            end do
        end do
    end subroutine sort_array

end program collatz_odds