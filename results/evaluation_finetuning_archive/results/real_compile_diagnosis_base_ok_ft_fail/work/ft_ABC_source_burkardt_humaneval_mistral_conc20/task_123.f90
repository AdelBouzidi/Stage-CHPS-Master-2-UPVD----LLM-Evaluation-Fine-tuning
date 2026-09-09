program collatz_odd
  implicit none
  integer :: n
  integer, allocatable :: odd_collatz(:)
  integer :: i, temp, count

  read(*,*) n

  count = 0
  temp = n
  do while (temp > 0)
    if (mod(temp, 2) == 1) then
      count = count + 1
    end if
    if (mod(temp, 2) == 0) then
      temp = temp / 2
    else
      temp = 3 * temp + 1
    end if
  end do

  allocate(odd_collatz(count))
  i = 0
  temp = n
  do while (temp > 0)
    if (mod(temp, 2) == 1) then
      i = i + 1
      odd_collatz(i) = temp
    end if
    if (mod(temp, 2) == 0) then
      temp = temp / 2
    else
      temp = 3 * temp + 1
    end if
  end do

  call sort_array(odd_collatz)

  write(*,*) odd_collatz

contains

  subroutine sort_array(arr)
    implicit none
    integer, intent(inout), allocatable :: arr(:)
    integer :: i, j, temp
    do i = 1, size(arr) - 1
      do j = i + 1, size(arr)
        if (arr(i) > arr(j)) then
          temp = arr(i)
          arr(i) = arr(j)
          arr(j) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program collatz_odd