program get_odd_collatz_demo
  implicit none
  integer :: n
  integer, allocatable :: result(:)
  
  ! Read input
  read(*,*) n
  
  ! Call the function
  result = get_odd_collatz(n)
  
  ! Print output
  print *, result
contains

  function get_odd_collatz(n) result(res)
    implicit none
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    integer :: count = 0
    
    ! Calculate the Collatz sequence and count odd numbers
    temp = n
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        count = count + 1
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    if (mod(n, 2) /= 0) then
      count = count + 1
    end if
    
    allocate(res(count))
    i = 0
    temp = n
    do while (temp /= 1)
      if (mod(temp, 2) /= 0) then
        i = i + 1
        res(i) = temp
      end if
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    if (mod(n, 2) /= 0) then
      i = i + 1
      res(i) = n
    end if
    
    ! Sort the result array
    call sort_array(res)
  end function get_odd_collatz

  subroutine sort_array(arr)
    implicit none
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

end program get_odd_collatz_demo