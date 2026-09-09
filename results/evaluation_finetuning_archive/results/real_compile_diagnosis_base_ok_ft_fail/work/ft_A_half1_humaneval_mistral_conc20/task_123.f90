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
    integer, intent(in) :: n
    integer, allocatable :: res(:)
    integer :: i, temp
    integer :: count
    
    ! Initialize result array
    count = 0
    temp = n
    do
      if (mod(temp, 2) == 1) then
        count = count + 1
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    
    allocate(res(count))
    i = 0
    temp = n
    do
      if (mod(temp, 2) == 1) then
        i = i + 1
        res(i) = temp
      end if
      if (temp == 1) exit
      if (mod(temp, 2) == 0) then
        temp = temp / 2
      else
        temp = 3 * temp + 1
      end if
    end do
    
    ! Sort the result array
    call sort_array(res, count)
  end function get_odd_collatz

  subroutine sort_array(arr, n)
    integer, intent(inout) :: arr(:)
    integer, intent(in) :: n
    integer :: i, j, temp
    
    do i = 1, n - 1
      do j = i + 1, n
        if (arr(j) < arr(i)) then
          temp = arr(i)
          arr(i) = arr(j)
          arr(j) = temp
        end if
      end do
    end do
  end subroutine sort_array

end program get_odd_collatz_demo