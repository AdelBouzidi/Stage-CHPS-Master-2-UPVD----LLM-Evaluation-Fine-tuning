program collatz_odd
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  integer :: i

  ! Read input
  read(*,*) n

  ! Initialize result array
  allocate(result(n))
  result = 0

  ! Calculate Collatz sequence odd numbers
  i = 1
  do while (n /= 1)
    if (mod(n, 2) /= 0) then
      result(i) = n
      i = i + 1
    end if
    if (mod(n, 2) == 0) then
      n = n / 2
    else
      n = 3 * n + 1
    end if
  end do

  ! Sort the result array
  call sort_array(result, i-1)

  ! Output result
  write(*,*) result(1:i-1)

contains

  subroutine sort_array(arr, n)
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: n
    integer :: i, j, temp
    do i = 1, n
      do j = i + 1, n
        if (arr(j) < arr(i)) then
          temp = arr(i)
          arr(i) = arr(j)
          arr(j) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program collatz_odd